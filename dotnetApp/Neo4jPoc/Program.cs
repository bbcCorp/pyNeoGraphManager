using System;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Neo4j.Driver;
using BBC.Neo4j;
using System.Threading.Tasks;

namespace Neo4jPoc
{
    class Program
    {
        static void Main(string[] args)
        {
            var loggerFactory = LoggerFactory.Create(builder =>
            {
                builder
                    .AddFilter("Microsoft", LogLevel.Warning)
                    .AddFilter("System", LogLevel.Warning)
                    .AddFilter("Neo4jPoc", LogLevel.Debug)
                    .AddFilter("BBC.Neo4j", LogLevel.Trace)
                    .AddConsole();
            });

            TestNeo4j(loggerFactory).Wait();

            loggerFactory = null;
        }
    
        static async Task TestNeo4j(ILoggerFactory loggerFactory)
        {

            var gm = new NeoGraphManager(
                loggerFactory.CreateLogger<NeoGraphManager>(), 
                "bolt://localhost:7687", "neo4j", "password");
            try
            {
                // Clear all Greeting nodes
                var resetDbQuery = "MATCH (n:Greeting) DELETE n ";
                await gm.ExecuteNonQuery(resetDbQuery);  
                Console.WriteLine("Removed all Greeting nodes and relationships");

                // Create a greeting node
                var query = "CREATE (a:Greeting{message: $message, createdBy: $user, createdOn: TIMESTAMP() }) ";
                await gm.ExecuteNonQuery(query, new { message = "hello, world" , user= "bbc" });  

                // Update the greeting node
                query = "MERGE (a:Greeting) " +
                    " ON CREATE SET a.createdOn= TIMESTAMP(), a.createdBy=$user " + 
                    " ON  MATCH SET a.updatedOn= TIMESTAMP(), a.updatedBy=$user " + 
                    " SET a.message= $message " +                
                    " RETURN a.message + ', from node ' + id(a)";

                var greeting= await gm.ExecuteScalar<String>(query, new { message = "hello, world" , user= "bbc" });  
                Console.WriteLine(greeting);  

                // Get count of the greeting node
                query = "MATCH (n:Greeting) return COUNT(n)";
                var count= await gm.ExecuteScalar<int>(query);  
                Console.WriteLine($"Count of nodes: {count}");  

                query = "CREATE (n:Greeting{message: $message, createdBy: $user, createdOn: TIMESTAMP() }) return id(n)";
                var nodeid = await gm.ExecuteScalar<int>(query, new { message = "hello, bbc" , user= "bbc1" });
                Console.WriteLine($"Created node#{nodeid}");  

                // Get count of the greeting node created by a certain user
                query = "MATCH (n:Greeting) WHERE n.createdBy =~'(?i)bbc.*' return COUNT(n)";
                count= await gm.ExecuteScalar<int>(query);  
                Console.WriteLine($"Count of nodes: {count}");


                // Get all messages of type:Greeting as a List of Tuples
                Console.WriteLine($"Fetching all messages"); 
                query = "MATCH (n:Greeting) return id(n) as id, n.message as msg";
                var messages= await gm.FetchRecords<Tuple<int,string>>(
                    cypherQuery:query, 
                    queryParams: new {}, 
                    recordProcessor:record =>  Tuple.Create(record["id"].As<int>(), record["msg"].As<string>())
                );  
                foreach(var msg in messages){
                    Console.WriteLine($" node#{msg.Item1} : {msg.Item2}"); 
                }

                // Get all messages of type:Greeting as a stream of buffered List of Tuples
                Console.WriteLine($"====== Performing buffered reads of all messages ======= "); 
                query = "MATCH (n) return id(n) as id";

                var fetchRecordBuffer = gm.FetchRecordsAsStream<Tuple<int>>(
                    cypherQuery:query, 
                    bufferSize: 10,
                    queryParams: new {}, 
                    recordProcessor:record =>  Tuple.Create(record["id"].As<int>())
                );

                await foreach(var messageBuffer in fetchRecordBuffer){
                    Console.WriteLine("Fetching next set of records ...");

                    foreach(var msg in messageBuffer){
                        Console.WriteLine($" node#{msg.Item1}"); 
                    }
                }
                

                await gm.ExecuteNonQuery(resetDbQuery);  
                Console.WriteLine("Removed all Greeting nodes and relationships");
            }
            catch(Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
            finally
            {
                gm.Dispose();                
            }

            return;
        }
    }
}

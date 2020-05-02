using System;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Neo4j.Driver;
using BBC.Neo4j;

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

            var gm = new NeoGraphManager(
                loggerFactory.CreateLogger<NeoGraphManager>(), 
                "bolt://localhost:7687", "neo4j", "password");

            try
            {
                // Clear all Greeting nodes
                var resetDbQuery = "MATCH (n:Greeting) DETACH DELETE n; ";
                gm.ExecuteNonQuery(resetDbQuery).Wait();  
                Console.WriteLine("Removed all Greeting nodes and relationships");

                // Create a greeting node
                var query = "CREATE (a:Greeting{message: $message, createdBy: $user, createdOn: TIMESTAMP() }) ";
                gm.ExecuteNonQuery(query, new { message = "hello, world" , user= "bbc" }).Wait();  

                // Update the greeting node
                var scalarQuery = "MERGE (a:Greeting) " +
                    " ON CREATE SET a.createdOn= TIMESTAMP(), a.createdBy=$user " + 
                    " ON  MATCH SET a.updatedOn= TIMESTAMP(), a.updatedBy=$user " + 
                    " SET a.message= $message " +                
                    " RETURN a.message + ', from node ' + id(a)";

                var greeting= gm.ExecuteScalar<String>(scalarQuery, new { message = "hello, world" , user= "bbc" }).Result;  
                Console.WriteLine(greeting);  

                // Get count of the greeting node
                scalarQuery = "MATCH (n:Greeting) return COUNT(n)";
                var count= gm.ExecuteScalar<int>(scalarQuery).Result;  
                Console.WriteLine($"Count of nodes: {count}");  

                gm.ExecuteNonQuery(resetDbQuery).Wait();  
                Console.WriteLine("Removed all Greeting nodes and relationships");
            }
            catch(Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
            finally
            {
                gm.Dispose();
                loggerFactory = null;
            }

        }
    }
}

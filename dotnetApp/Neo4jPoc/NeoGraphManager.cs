using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Neo4j.Driver;

namespace BBC.Neo4j
{
    public class NeoGraphManager : IDisposable
    {
        private readonly Microsoft.Extensions.Logging.ILogger _logger;
        private readonly IDriver _driver;
        private readonly string _database;

        public NeoGraphManager(ILogger<NeoGraphManager> logger, String uri, String user, String password, string database="neo4j")
        {
            _logger = logger;
            
            _driver = GraphDatabase.Driver(uri, AuthTokens.Basic(user, password));

            _database = database;
        }

        public async Task ExecuteNonQuery(string cypherQuery, object queryParams=null)
        {
            IAsyncSession session = _driver.AsyncSession(o => o.WithDatabase(this._database));

            if(queryParams == null)
            {
                queryParams= new {};
            }

            try
            {
                _logger.LogDebug($"Executing query: {cypherQuery}");

                IResultCursor cursor = await session.RunAsync(cypherQuery, queryParams);

                IResultSummary result = await cursor.ConsumeAsync();

                _logger.LogTrace($"Query executed successfully.");
                
            }
            catch(Exception ex)
            {
                Console.WriteLine($"Error executing query. {ex.Message}");
                throw;
            }
            finally
            {
                await session.CloseAsync();
            }
        }

        public async Task<T> ExecuteScalar<T>(string cypherQuery, object queryParams=null)
        {
            T result = default(T);
            IAsyncSession session = _driver.AsyncSession(o => o.WithDatabase(this._database));

            _logger.LogDebug($"Executing query: {cypherQuery}");
            
            if(queryParams == null)
            {
                queryParams= new {};
            }

            try
            {     

                IResultCursor resultCursor = await session.RunAsync(cypherQuery, queryParams);

                IRecord record = await resultCursor.SingleAsync();

                result = record[0].As<T>();

                _logger.LogDebug("Query executed successfully");
                
            }
            catch(Exception ex)
            {
                _logger.LogError(ex, $"Error executing query. {ex.Message}");
                throw;
            }
            finally
            {
                await session.CloseAsync();
                
            }

            return result;
        }

        // Get all records as a List
        public async Task<List<T>> FetchRecords<T>(Func<IRecord, T> recordProcessor, string cypherQuery, object queryParams=null)
        {
            List<T> result = null;
            IAsyncSession session = _driver.AsyncSession(o => o.WithDatabase(this._database));

            _logger.LogDebug($"Executing query: {cypherQuery}");
            
            if(queryParams == null)
            {
                queryParams= new {};
            }

            try
            {     

                IResultCursor resultCursor = await session.RunAsync(cypherQuery, queryParams);

                result = await resultCursor.ToListAsync(record => recordProcessor(record));

                _logger.LogDebug("Query executed successfully");
                
            }
            catch(Exception ex)
            {
                _logger.LogError(ex, $"Error executing query. {ex.Message}");
                throw;
            }
            finally
            {
                await session.CloseAsync();
                
            }

            return result;
        }

        // Get records as a stream of buffered List
        public async IAsyncEnumerable<List<T>> FetchRecordsAsStream<T>(
            Func<IRecord, T> recordProcessor, 
            string cypherQuery, object queryParams=null, 
            long bufferSize=100)
        {
            long recordsProcessed = 0;

            List<T> resultBuffer = new List<T>();
            IAsyncSession session = _driver.AsyncSession(o => o.WithDatabase(this._database));

            _logger.LogDebug($"Executing query: {cypherQuery}");
            
            if(queryParams == null)
            {
                queryParams= new {};
            }

            try
            {     

                IResultCursor resultCursor = await session.RunAsync(cypherQuery, queryParams);

                _logger.LogDebug("Reading cursor");

                while (await resultCursor.FetchAsync())
                {
                    recordsProcessed += 1;

                    resultBuffer.Add( recordProcessor(resultCursor.Current));
                    
                    if(resultBuffer.Count >= bufferSize)
                    {
                        _logger.LogDebug($"Records processed: {recordsProcessed} ...");
                        yield return resultBuffer;
                        resultBuffer.Clear();
                    }
                }

                _logger.LogDebug($"* Total records processed: {recordsProcessed} *");
                yield return resultBuffer;
                                            
            }
            finally
            {
                await session.CloseAsync();
                
            }
        }


        public void Dispose()
        {
            _driver?.Dispose();
        }
    }
}

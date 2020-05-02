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

                await cursor.ConsumeAsync();

                _logger.LogDebug("Query executed successfully");
                
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

        public void Dispose()
        {
            _driver?.Dispose();
        }
    }
}

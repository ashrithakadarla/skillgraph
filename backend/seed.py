import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("COGNODB_URI")
USER = os.getenv("COGNODB_USER")
PASSWORD = os.getenv("COGNODB_PASSWORD")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


def seed_database(tx):
    # Clear existing data
    tx.run("MATCH (n) DETACH DELETE n")

    # Developers
    tx.run("""
        CREATE
        (a:Developer {name: 'Ashritha', role: 'Full-Stack Developer'}),
        (r:Developer {name: 'Rahul', role: 'Backend Developer'}),
        (s:Developer {name: 'Sneha', role: 'Frontend Developer'})
        RETURN count(*) AS created
    """)

    # Skills
    tx.run("""
        CREATE
        (java:Skill {name: 'Java'}),
        (python:Skill {name: 'Python'}),
        (react:Skill {name: 'React'}),
        (fastapi:Skill {name: 'FastAPI'}),
        (sql:Skill {name: 'SQL'})
        RETURN count(*) AS created
    """)

    # Projects
    tx.run("""
        CREATE
        (airmind:Project {
            name: 'AirMind AI',
            description: 'Urban air quality intelligence platform'
        }),
        (secure:Project {
            name: 'SecureRAG',
            description: 'Prompt injection defense framework'
        }),
        (shop:Project {
            name: 'SmartShop',
            description: 'E-commerce recommendation application'
        })
        RETURN count(*) AS created
    """)

    # Technologies
    tx.run("""
        CREATE
        (mongo:Technology {name: 'MongoDB'}),
        (fastapiTech:Technology {name: 'FastAPI'}),
        (reactTech:Technology {name: 'React'}),
        (neo4j:Technology {name: 'Neo4j'}),
        (docker:Technology {name: 'Docker'})
        RETURN count(*) AS created
    """)

    # Developer -> Skills
    tx.run("""
        MATCH
        (a:Developer {name: 'Ashritha'}),
        (r:Developer {name: 'Rahul'}),
        (s:Developer {name: 'Sneha'}),
        (java:Skill {name: 'Java'}),
        (python:Skill {name: 'Python'}),
        (react:Skill {name: 'React'}),
        (fastapi:Skill {name: 'FastAPI'}),
        (sql:Skill {name: 'SQL'})

        CREATE
        (a)-[:HAS_SKILL]->(java),
        (a)-[:HAS_SKILL]->(python),
        (a)-[:HAS_SKILL]->(fastapi),
        (r)-[:HAS_SKILL]->(python),
        (r)-[:HAS_SKILL]->(sql),
        (s)-[:HAS_SKILL]->(react),
        (s)-[:HAS_SKILL]->(sql)
        
        RETURN count(*) AS created
    """)

    # Developer -> Projects
    tx.run("""
        MATCH
        (a:Developer {name: 'Ashritha'}),
        (r:Developer {name: 'Rahul'}),
        (s:Developer {name: 'Sneha'}),
        (airmind:Project {name: 'AirMind AI'}),
        (secure:Project {name: 'SecureRAG'}),
        (shop:Project {name: 'SmartShop'})

        CREATE
        (a)-[:WORKED_ON]->(airmind),
        (a)-[:WORKED_ON]->(secure),
        (r)-[:WORKED_ON]->(airmind),
        (r)-[:WORKED_ON]->(shop),
        (s)-[:WORKED_ON]->(shop)
        RETURN count(*) AS created
    """)

    # Skills -> Projects
    tx.run("""
        MATCH
        (python:Skill {name: 'Python'}),
        (fastapi:Skill {name: 'FastAPI'}),
        (java:Skill {name: 'Java'}),
        (react:Skill {name: 'React'}),
        (sql:Skill {name: 'SQL'}),
        (airmind:Project {name: 'AirMind AI'}),
        (secure:Project {name: 'SecureRAG'}),
        (shop:Project {name: 'SmartShop'})

        CREATE
        (python)-[:USED_IN]->(airmind),
        (fastapi)-[:USED_IN]->(airmind),
        (python)-[:USED_IN]->(secure),
        (java)-[:USED_IN]->(secure),
        (react)-[:USED_IN]->(shop),
        (sql)-[:USED_IN]->(shop)
        RETURN count(*) AS created
    """)

    # Projects -> Technologies
    tx.run("""
        MATCH
        (airmind:Project {name: 'AirMind AI'}),
        (secure:Project {name: 'SecureRAG'}),
        (shop:Project {name: 'SmartShop'}),
        (mongo:Technology {name: 'MongoDB'}),
        (fastapi:Technology {name: 'FastAPI'}),
        (react:Technology {name: 'React'}),
        (neo4j:Technology {name: 'Neo4j'}),
        (docker:Technology {name: 'Docker'})

        CREATE
        (airmind)-[:USES]->(mongo),
        (airmind)-[:USES]->(fastapi),
        (secure)-[:USES]->(neo4j),
        (secure)-[:USES]->(docker),
        (shop)-[:USES]->(react),
        (shop)-[:USES]->(mongo)
        RETURN count(*) AS created
    """)


with driver.session() as session:
    session.execute_write(seed_database)

print("✅ Graph database seeded successfully!")

driver.close()
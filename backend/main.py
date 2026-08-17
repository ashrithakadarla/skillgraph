import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("COGNODB_URI")
USER = os.getenv("COGNODB_USER")
PASSWORD = os.getenv("COGNODB_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD)
)

app = FastAPI(title="SkillGraph API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "SkillGraph API is running"}


@app.get("/developers")
def get_developers():
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (d:Developer)
                RETURN d.name AS name, d.role AS role
                ORDER BY d.name
            """)

            return [record.data() for record in result]

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )


@app.get("/developer/{name}")
def get_developer(name: str):
    try:
        with driver.session() as session:

            developer = session.run("""
                MATCH (d:Developer {name: $name})
                RETURN d.name AS name, d.role AS role
            """, name=name).single()

            if not developer:
                raise HTTPException(
                    status_code=404,
                    detail="Developer not found"
                )

            skills = session.run("""
                MATCH (d:Developer {name: $name})
                      -[:HAS_SKILL]->(s:Skill)
                RETURN s.name AS name
                ORDER BY s.name
            """, name=name)

            projects = session.run("""
                MATCH (d:Developer {name: $name})
                      -[:WORKED_ON]->(p:Project)
                RETURN p.name AS name, p.description AS description
                ORDER BY p.name
            """, name=name)

            return {
                "name": developer["name"],
                "role": developer["role"],
                "skills": [r["name"] for r in skills],
                "projects": [r.data() for r in projects]
            }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )


@app.get("/developer/{name}/connections")
def get_connections(name: str):
    try:
        with driver.session() as session:

            result = session.run("""
                MATCH (d:Developer {name: $name})
                      -[:WORKED_ON]->(p:Project)
                      -[:USES]->(t:Technology)
                RETURN p.name AS project,
                       collect(t.name) AS technologies
                ORDER BY p.name
            """, name=name)

            return [record.data() for record in result]

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )
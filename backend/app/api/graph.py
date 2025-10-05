# backend/app/api/graph.py
from fastapi import APIRouter
from neo4j import GraphDatabase
import os

router = APIRouter()

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "testpassword"
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

@router.get("/graph")
def get_graph():
    query = """
    MATCH (p:Publication)-[:HAS_SUMMARY]->(s:Summary)-[:MENTIONS]->(e:Entity)
    RETURN p.title AS title, s.text AS summary, collect(e.name) AS entities LIMIT 50
    """
    with driver.session() as session:
        result = session.run(query)
        data = []
        for record in result:
            data.append({
                "title": record["title"],
                "summary": record["summary"],
                "entities": record["entities"]
            })
    return data


🚧 Project Status: In Progress
This repository is under active development. Features, structure, and documentation may change frequently. Feedback is welcome!

🧠 Project: Economy Stats AI
Overview

A FastAPI-based backend system for fetching, storing, and analyzing news articles related to economic topics. The project integrates external APIs, asynchronous processing, and intelligent agent logic to surface relevant insights.

🔧 Tech Stack

FastAPI with async routes and lifespan events

SQLAlchemy Async ORM with SQLite (PostgreSQL-ready)

Dependency Injection via FastAPI Depends

Pydantic schemas for validation

Custom Agents for content selection and editing logic

Structured Logging, error handling, and modular design

🧩 Features

Accepts POST requests with topic, from_date, and to_date to drive pipeline execution

Uses news APIs to fetch articles, stores them conditionally in a relational database

Implements a selector-editor agent pipeline for filtering and modifying articles

Stores only articles with complete metadata (quality-controlled)

Fully asynchronous database operations using SQLAlchemy 2.0

📦 Architecture Highlights

Dependency injection for clean separation of concerns

Context object for managing state across request lifecycle

Pipeline split into clear modules: API ingestion → DB storage → Agent processing

Modular, testable structure with routers, services, schemas, and core

🚀 Key Takeaways

This project showcases:

Deep understanding of FastAPI internals, async programming, and real-world data flow

Ability to manage application state and integrate external services

Hands-on experience with production-ready architecture patterns

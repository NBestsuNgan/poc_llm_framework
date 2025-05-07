# Database & Data Lake

## Table of Contents
- [Vector Database](#vector-database)
- [SQL Database](#sql-database)
- [Data Lake](#data-lake)


### Vector Database

Vector databases differ from traditional relational databases in that they don't offer a graphical user interface (GUI) for browsing or managing data. Instead, they store data in *collections*, where each collection can contain many entries (or vectors). These entries support *flexible, schema-less properties*, allowing for dynamic formats tailored to similarity-based search and retrieval.

### SQL Database

SQL databases, such as MySQL, PostgreSQL, or Oracle, use a structured, table-based format with predefined schemas. They are ideal for managing structured data and support powerful query capabilities using SQL (Structured Query Language). Unlike vector databases, SQL databases offer robust GUIs and tools for data browsing, analytics, and relational integrity, making them suitable for transactional systems and well-defined data models.

### Data Lake

![data_lake](/resource/iamges/database_datalake/data_lake.png "data_lake")

A data lake is a centralized repository for storing large volumes of data in raw or semi-structured formats. In the image above, MinIO is used as a blob storage system—commonly referred to as a *data lake*—which can store files in various formats. These are often used to retain outputs from processing pipelines, intermediate files, logs, or any assets associated with business or analytical workflows.

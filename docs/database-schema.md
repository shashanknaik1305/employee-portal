# Database Schema

## Table: users

| Column | Data Type | Constraints | Description |
|---------|-----------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Unique user ID |
| name | VARCHAR(100) | NOT NULL | User's full name |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email |
| password_hash | TEXT | NOT NULL | Encrypted password |
| profile_photo | TEXT | NULL | Uploaded profile photo path |
| resume_file | TEXT | NULL | Uploaded resume path |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation time |

---

## SQL

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    profile_photo TEXT,
    resume_file TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
CREATE TABLE job_snapshots (
    snapshot_id SERIAL PRIMARY KEY,
    job_id VARCHAR(50),
    snapshot_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- Skill Demand Historical Snapshots
-- =====================================

CREATE TABLE IF NOT EXISTS skill_demand_snapshots (

    snapshot_id SERIAL PRIMARY KEY,

    snapshot_date DATE NOT NULL,

    skill_id INTEGER NOT NULL,

    job_count INTEGER NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_skill_snapshot_skill

    FOREIGN KEY(skill_id)

    REFERENCES skills(skill_id)

);



-- =====================================
-- Taxonomy Demand Historical Snapshots
-- =====================================

CREATE TABLE IF NOT EXISTS taxonomy_demand_snapshots (

    snapshot_id SERIAL PRIMARY KEY,

    snapshot_date DATE NOT NULL,

    taxonomy_id INTEGER NOT NULL,

    job_count INTEGER NOT NULL,

    skill_count INTEGER NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_taxonomy_snapshot_taxonomy

    FOREIGN KEY(taxonomy_id)

    REFERENCES skill_taxonomy(taxonomy_id)

);
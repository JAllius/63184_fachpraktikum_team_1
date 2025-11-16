-- Core schema for MySQL 8
CREATE TABLE IF NOT EXISTS datasets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  owner VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dataset_versions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  dataset_id INT NOT NULL,
  uri TEXT NOT NULL,
  schema_json JSON,
  profile_json JSON,
  row_count INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (dataset_id) REFERENCES datasets(id)
);

CREATE TABLE IF NOT EXISTS ml_problems (
  id INT AUTO_INCREMENT PRIMARY KEY,
  dataset_version_id INT NOT NULL,
  task VARCHAR(64) NOT NULL,
  target VARCHAR(255) NOT NULL,
  feature_strategy_json JSON,
  validation_strategy VARCHAR(128),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (dataset_version_id) REFERENCES dataset_versions(id)
);

CREATE TABLE IF NOT EXISTS models (
  id INT AUTO_INCREMENT PRIMARY KEY,
  problem_id INT NOT NULL,
  name VARCHAR(255),
  framework_algorithm VARCHAR(128),
  status VARCHAR(32) NOT NULL,
  metrics_json JSON,
  model_uri TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (problem_id) REFERENCES ml_problems(id)
);

CREATE TABLE IF NOT EXISTS jobs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  type VARCHAR(32) NOT NULL,
  problem_id INT,
  model_id INT,
  status VARCHAR(32) NOT NULL,
  started_at TIMESTAMP NULL,
  finished_at TIMESTAMP NULL,
  error TEXT,
  FOREIGN KEY (problem_id) REFERENCES ml_problems(id),
  FOREIGN KEY (model_id) REFERENCES models(id)
);

CREATE TABLE IF NOT EXISTS predictions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  problem_id INT NOT NULL,
  model_id INT NOT NULL,
  job_id INT NULL,
  inputs_json JSON,
  outputs_json JSON,
  outputs_uri TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (problem_id) REFERENCES ml_problems(id),
  FOREIGN KEY (model_id) REFERENCES models(id),
  FOREIGN KEY (job_id) REFERENCES jobs(id)
);

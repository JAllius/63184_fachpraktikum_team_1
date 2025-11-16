INSERT INTO datasets (name, owner)
VALUES ('sales_store_1', 'team1');

INSERT INTO dataset_versions (dataset_id, uri, schema_json, row_count)
VALUES (1, '/data/sales_2025_01.csv', JSON_OBJECT('date','DATE','sales','INT'), 1000);

-- Example problem (timeseries forecasting sales)
INSERT INTO ml_problems (dataset_version_id, task, target, feature_strategy_json, validation_strategy)
VALUES (1, 'timeseries', 'sales', JSON_OBJECT('include', JSON_ARRAY('date')), 'train_test_split');

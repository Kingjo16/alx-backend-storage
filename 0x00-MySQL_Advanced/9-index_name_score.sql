-- Index idx_name_first_score on the table names and the first letter
CREATE INDEX idx_name_first_score ON names(name(1), score);

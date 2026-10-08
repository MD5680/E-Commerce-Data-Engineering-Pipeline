-- =========================================
-- DATABASE SETUP
-- E-Commerce Data Engineering Project
-- =========================================

-- Create database
CREATE DATABASE IF NOT EXISTS ECOMMERCE_DB;


-- Create schemas
CREATE SCHEMA IF NOT EXISTS ECOMMERCE_DB.RAW;

CREATE SCHEMA IF NOT EXISTS ECOMMERCE_DB.STAGING;

CREATE SCHEMA IF NOT EXISTS ECOMMERCE_DB.ANALYTICS;


-- Verify schemas
SHOW SCHEMAS IN DATABASE ECOMMERCE_DB;
# Stock Correlation Analysis Tool

This project was developed as a group project. I contributed to the time series data pipeline, stock visualization, correlation analysis, and reporting components.

## Overview

A Python-based financial analysis project designed to examine the relationship between two stocks using historical market data. This tool collects one year of OHLC (Open, High, Low, Close) data through the Yahoo Finance API and performs time series analysis to compare stock movements over time.

## Features

- Built a time series data pipeline using the Yahoo Finance API to process 365 days of historical OHLC data
- Visualized synchronized daily price movements of two stocks over the same time period
- Applied Pearson correlation and linear regression to measure the relationship between chronologically aligned stock data
- Generated scatter plots with regression lines to visually evaluate day-by-day correlation between securities
- Automated analysis reporting with correlation interpretation and time series charts for investment insights

## Tech Stack

- Python
- Yahoo Finance API (`yfinance`)
- Pandas
- Matplotlib
- SciPy

## Project Purpose

The goal of this project is to help users compare the performance and co-movement of two stocks over time through statistical analysis and clear visualizations. By combining time series data processing, regression modeling, and automated reporting, the tool provides a simple way to explore potential relationships between securities.

## Example Analysis Workflow

1. Retrieve one year of historical stock price data
2. Align both datasets by date
3. Plot each stock’s daily price movement over time
4. Calculate Pearson correlation and linear regression
5. Generate scatter plots and summary interpretations

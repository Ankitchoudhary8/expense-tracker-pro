# Expense Tracker Pro — Portfolio Case Study

**Live application:** https://expense-tracker-pro-1-595b.onrender.com  
**Source code:** https://github.com/Ankitchoudhary8/expense-tracker-pro

## Overview

Expense Tracker Pro is a responsive full-stack web application for recording expenses, viewing spending trends, filtering transactions, and tracking monthly budgets.

## Problem

Personal expenses are easy to lose track of when they are recorded in scattered notes or not categorized. This project brings transaction management and spending summaries into one interface.

## Solution

- Flask backend with REST endpoints for expense and budget management
- SQLite persistence in the current implementation
- JavaScript dashboard with category and monthly spending charts
- Filtering by month and category, plus CSV export
- Authentication for access to the hosted dashboard
- GitHub Actions checks and Render web-service deployment

## Technical Highlights

- Separation of backend API, database layer, and frontend assets
- Expense create/read/update/delete workflows
- Browser-rendered summaries and visualizations
- Automated Python API tests and JavaScript syntax checks
- Production server configuration using Gunicorn

## Deployment

The application is live on Render. The current SQLite database is **not guaranteed to persist** on an ephemeral service filesystem. Persistent storage is required before using the application for important personal finance records.

## Validation Status

The hosted sign-in and dashboard have been visually confirmed. Full end-to-end verification of expense editing, budget calculations, export, and responsive layouts is pending. A previous screenshot suggested a possible discrepancy in budget totals, so the budget calculation should not yet be considered verified.

## Resume Bullets

- Built and deployed a full-stack expense-tracking dashboard using Python, Flask, JavaScript, and SQLite.
- Implemented transaction management, monthly budgets, category filters, data visualizations, and CSV export.
- Configured automated CI checks with GitHub Actions and deployed the Flask service using Gunicorn on Render.

## Future Improvements

1. Move expense and budget data to durable managed storage.
2. Add regression tests for budget totals and all authenticated workflows.
3. Improve user account management and session security.
4. Capture sanitized desktop and mobile screenshots for the project README.

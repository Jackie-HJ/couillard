# Couillard Solar Foundation: Deerfield Solar Project Impact

This project will visualize solar output data from 7 solar arrays in Deerfield, WI. It will show what a small community can achieve with solar, which will help to convince other small communities to adopt it. Couillard would also like more detailed information for administrative users.

## Project Management

The work that needs to be done on this project is kept track of by [the issues on this repository](https://github.com/DSSD-Madison/couillard/issues). To contribute, create a new branch, make your changes, push, then make a pull request into main. The main branch is protected so that it can only be modified through merged pull requests, and pull requests can only be merged if at least one person approves it.

## Problem and System Design

The 7 arrays do not all use the same inverters, so the data collected is stored in different places. The challange will be bringing all the data into one place.

Backend: Python script cron job deployed to Render

Database: Firebase Firestore, same schema as Helios project

Auth (if needed): Firebase Auth

Frontend: React + GitHub pages / Firebase Hosting

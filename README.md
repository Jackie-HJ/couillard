# Couillard Solar Foundation: Deerfield Solar Analytics

This project will visualize solar output data from 7 solar arrays in Deerfield, WI. It will show what a small community can achieve with solar, which will help to convince other small communities to adopt it. Couillard would also like more detailed information for administrative users.

## Project Management

The work that needs to be done on this project is kept track of by [the issues on this repository](https://github.com/DSSD-Madison/couillard/issues). To contribute, choose an issue (or multiple) to tackle and assign it to yourself so other people know that someone is working on it already. Create a new branch, make your changes, push, then make a pull request into main with the issue(s) linked. The main branch is protected so that it can only be modified through merged pull requests, and pull requests can only be merged if at least one person approves it.

## Problem and System Design

The 7 arrays do not all use the same inverters, so the data collected is stored in different places. The challenge will be bringing all the data into one place.

Backend: 
- Database: Firebase Firestore, same schema as [Helios Firestore](https://console.firebase.google.com/project/helios-9d435/firestore)
- Python script cron job with GitHub Actions that runs every day. Populates db with last days worth of data, or all past data if a field `needs_update` is set on the array's document (it unsets it after populating).
- [Admin Spreadsheet](https://docs.google.com/spreadsheets/d/1S9nvMsymOAseaOQ_cnDN_oBePvDAuavbSKx_wkPa8Bk) where admins can add new arrays (create document and set `needs_update`) or just force an update on an array (update array document with `needs_update`). Uses Google Apps Script functions triggered on button clicks.

Frontend: 
- Query Firestore similar to [how it's done for Helios](https://github.com/DSSD-Madison/Helios/blob/main/frontend/helios-dashboard/src/routes/Dashboard/FetchData.js)
- Highlights of energy generated to date; Graph of energy produced over time; images and descriptions

[Link to Firebase console for this project](https://console.firebase.google.com/project/couillard-b61b8/overview)

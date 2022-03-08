# University of Minnesota graduate worker pay analysis

## Background
  - The University of Minnesota is a public institution, and so all of the pay data for employees is available online
  - We have downloaded this data for 95XX job codes, which (hopefully) comprises the entire graduate assistant population

## Goals
  - Present data analysis at COGS
  - Present data on a website
  - In the data, want to accurately represent pay data in each department
  - Operationally, this means that if any given graduate assistant looks at the pay that we have presented, they'll say "yeah, that looks about consistent with my pay"
  - We want to compare this reasonably accurate data to inflation as provided by the Bureau of Labor Statistics
  - Want people to leave the discussion with two ideas: (1) We are -- across the board -- just barely getting paid above the cost of living. (2) This year, we have received a pay cut of some percent (I think 4%). Why should we get that pay cut when Joan Gabel just got hundreds of thousands of dollars for a pay raise?
  - Want to establish a clear, data-driven narrative about how GA wages have stagnated across the board.

## Data analysis
  - Taken public data in snapshots every spring summer and fall going back to 2015.
  - This does include post docs, but there are only 4 employment classes
  - In each of those, we're only looking at "Employment Class" == "Graduate Assistants" so we filter out graduate assistants

## Problems
  - Some number of graduate students (unknown portion) receive fellowships over the summer which do not show up in the publicly available data
  - It is unclear whether the 95XX job codes completely comprise the graduate assistant population


## To do
  - Need to make sure that we are not including medical residents. They're represented by professional student government (instead of COGS). 
  - COGS does not represent professional student programs.

## Data sources


## Assumptions
  - Who is in the sample? anyone with a 95xx code whose employee class is graduate assistant
  - Must be working 20 hours a week total, summed over all their 95xx employments (folks identified by their student ID)
  - Only look at academic year -- for rationale: only about half of the students show up as getting paid during the summer in the data. Some aren't getting paid, some are being supported by fellowships which don't show up on data.
	  - We are campaigning for a minimum, so if unsupported during the summer aren't making enough to live, we need to campaign for that.
  

# FSI_Proj

1) Ignore the one 10-k file that is in here that's accidentally uploaded
2) Task1.py is 1.1, 1.2 is Analysis.py

1) Simple script that downloads the 10-k filings from 1995-2023. I chose Lazard, BNY Mellon, and JP Morgan because they all sort of occupy the same space in asset management. I wanted to look at the state of these firms based on risk factors identified over time. 
2) Risk factors are important for users in case they want to invest/buy stock in this specific company. I categorized the visualization generation into different risk factor categories such as brand reputation, security, financial, and operational. In this way, the users can see what the companies are most concerned about over a span of 1995-2023. In addition, users can see what has been improved. My goal was a stacked colored trend chart that would record the frequencies of different risk factor keywords mentioned over time. 

Image Attached: I had a category named "other" for risk factors that were not captured withint the limited amount of words I was able to come up with for each category. However it was a weak point because it completely overwhelmed the other categories.

Improvements: The Image generation takes a long time given the code (around 1 hour) but improvements I've made since the screenshot
    -Fixed x-y axis labels into actual years
    -Separate graphs for each ticker
    -Filtered the other category out so it doesn't overwhelm the other categories

Errors/Pain Points: I think a major pain point for this task was identifying errors in data extraction. I wanted to extract data about Risk Factors, and on first try I used the line: "if 'Item 1A. Risk Factors' in line:", but it took a lot of debugging to realize that it was the primary issue in extracting data from Lazard and JP Morgan, because each Risk Factor header was formatted differently with punctuations/spellings. In addition, using the current version "if 'Item 1A.' in line:" is sort of problematic because it will appear multiple times in irrelevant places and the code will start reading from places like the table of contents or headers, which makes the run-time exponentially longer. I think next time, I would choose a keyword/phrase that is more specific or I should focus on a smaller subsection such as 'CyberSecurity' rather than the entire Risk Factor section . 

Alternative Ideas for this:
    -Sentiment Analysis 
    -Regulatory Analysis -> Heat map or word Cloud


3) Task 1.3: Unfortunately I wasn't really able to completely deploy a simple app that would show visualizations based on given input, but I somewhat enfolded Task 2 and Task 1.2 together. 

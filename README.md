# HQBot
Bot to Google answers to HQ Trivia questions and help give answers

How it works:

1. Screenshots Bluestacks (IOS Emulator)
2. Uses Tesseract Image recognition to get the questions and answers from the screenshot
3. Uses Selenium with multithreading to do a series of Google searches for answers
  a. Googles the question and searches the page for answers
  b. Googles the question along with the answer after it to see how many results
4. Other stategies built in such as when the question contains "NOT" it reverses the order of which question it is
5. The User can pull up one of the firefox windows to see the Google results if they want to search the page themself
  a. This is much faster than typing the question into Google yourself

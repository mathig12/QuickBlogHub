-- Sample seed data for content publishing platform
-- Include examples of posts with different statuses

-- Draft posts
INSERT INTO posts (title, content, status) 
VALUES ('My First Draft Post', 'This is the content of my first draft post. It is still in progress and needs some work before submission.', 'draft');

INSERT INTO posts (title, content, status) 
VALUES ('Ideas for Next Week', 'Here are some ideas I want to write about: technology trends, AI ethics, and software development best practices.', 'draft');

-- Flagged posts (with reasons)
INSERT INTO posts (title, content, status, flagged_reasons) 
VALUES ('THIS IS MY ANGRY POST!', 'I AM VERY ANGRY ABOUT THIS TOPIC!!! IT MAKES ME SO MAD I JUST WANT TO SCREAM!', 'flagged', 'Aggressive tone detected (excessive use of capital letters), Aggressive tone detected (excessive exclamation marks)');

INSERT INTO posts (title, content, status, flagged_reasons) 
VALUES ('Short Post', 'Too short content.', 'flagged', 'Content too short (minimum 50 characters)');

INSERT INTO posts (title, content, status, flagged_reasons) 
VALUES ('Why I dislike certain things', 'I think some people are really stupid when they do certain things. It makes me so annoyed how dumb they can be!', 'flagged', 'Banned words detected: stupid, dumb');

-- Approved posts
INSERT INTO posts (title, content, status) 
VALUES ('The Future of AI', 'Artificial Intelligence is transforming the way we live and work. From virtual assistants to autonomous vehicles, AI technologies are becoming increasingly integrated into our daily lives. This article explores the potential future developments in AI and their implications for society.', 'approved');

INSERT INTO posts (title, content, status) 
VALUES ('Sustainable Living Tips', 'Living sustainably is crucial for the health of our planet. This post discusses simple steps everyone can take to reduce their environmental footprint, including reducing waste, conserving energy, and making mindful consumption choices.', 'approved');

-- Published posts
INSERT INTO posts (title, content, status) 
VALUES ('Introduction to FastAPI', 'FastAPI is a modern, fast web framework for building APIs with Python. It is based on standard Python type hints and offers automatic validation, serialization, and documentation. This post provides an overview of its key features and benefits for developers.', 'published');

INSERT INTO posts (title, content, status) 
VALUES ('Effective Time Management', 'Time management is a critical skill in todays fast-paced world. This article shares proven strategies for prioritizing tasks, avoiding procrastination, and maintaining a healthy work-life balance. By implementing these techniques, you can increase productivity while reducing stress.', 'published');

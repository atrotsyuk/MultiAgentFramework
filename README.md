A simple framework for a multi-agent conversation

Steps To Run:
1. Download and install docker desktop
2. open a terminal
3. navigate to your git repository location MultiAgentFramework
4. take a git pull from full-stack-app branch using:
5. git fetch origin full-stack-app:full-stack-app
6. then, git checkout full-stack-app
7. Now, Build a docker image using
8. docker build -t app .
9. then it will take some to build the docker image
10. Now run the docker image using
11. docker run -p 8000:8000 app
12. Then open a new browser window at http://localhost:8000/
13. Your app must be up and running
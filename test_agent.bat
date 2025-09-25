@echo off
echo Testing PULSE UK Agent...
echo.
curl -X POST https://pulse-agent-smcqmdg45a-uc.a.run.app -H "Content-Type: application/json" -d "{\"query\": \"What are the current UK cultural trends?\"}"
echo.
echo.
pause
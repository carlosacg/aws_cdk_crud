LINT_HELP_MESSAGE = "Tip:\nRun 'make lint-fix' to fix your code style or fix it manually\n"

lint-fix:
	@python -m black .
	@python -m isort --atomic . --profile black

synth:
	cdk synth

deploy:
	cdk deploy

# Architectural Decision Record

## Title: Example Title

- Status: [Proposed | Accepted | Rejected | Deprecated | Superseded]

### Context

[Describe the context and background of the decision]

### Decision

[Describe the decision that has been made]

### Consequences

[Describe the potential consequences of the decision]

### Alternatives

[Describe any alternative options that were considered]

### Related ADRs

[List any related ADRs, if applicable]

### References

[List any references or resources used in making the decision]


## Title: Initial Choice of Frameworks

- Status: Accepted

### Context

In the context of the case challenge, I need to implement a simplistic API within 1 week.
The requirements are formulated in an open fashion, for example not specifying specific required authentication methods, expected daily load and infrastructure requirements.

### Decision

Given the short time and open formulation, I decide to start with a simplistic setup to efficiently implement a first API and allow subsequent iterative improvement based on real bottlenecks as opposed to assumed requirements.

Therefore, I start with the following tech stack:
- GitHub as remote repository and collaboration tool.
- VS Code as my personal preference (I commit my config files to share with a potential team and demonstrate my abilities)
- Pixi for Python package management, as it allows ruff-based, quick package resolution of both pip and conda packages.
- FastAPI as modern API framework, to ensure fast iteration speed.
   - automatically generated OpenAPI documentation (preparing auto-generation of e.g. react.js code to connect the future frontend)
- SQLModel as ORM to ensure type validation and Python best practices
- SQLite database, given that the API load is not specified but likely limited given that the API is for internal usage
- As infrastructure and deployment was not yet specified, I start with a simplistic deployment via fly for demonstration purposes.
   - Based on further requirements, a deployment via Infrastructure-as-Code with Pulumi in Python is envisioned, to limit API access to the internal AWS VPCs.

### Consequences

- While pixi may become the strongest package management tool, it is still a bit unstable and beta, requiring a couple of small fixes or workarounds.
- VS Code config files are usually gitignored, so depending on the teams preferences, they may need to be removed from git history at a later point.
- Deploying the app to fly will expose it to the internet. So, I will use a random app name and URL such that the setup should be sufficiently anonymous for this case challenge.

### Alternatives

- Poetry is a widely used standard for Python package management, facilitating package definition and config via pyproject.toml. However, it does not support conda package resolution and is not yet ruff-based. Therefore, pixi may be considered the better option for a project that may want to leverage CUDA-based machine learning and thus may require conda packages.
- Flask would be another option to create the API. However, FastAPI is the more modern framework to create APIs.
- PyCharm is used by many Pythonistas and developers may prefer other IDEs. Given the choice for FastAPI and the preference of both its creator and myself for VS Code, I choose VS Code. However, each team member could choose their IDE.
- I could directly start with Postgres and Alembic for database and migrations. However, in the context of the case challenges and my limited resources, I decide to start with a more simplistic setup and potentially switch to the more sophisticated setup based on further requirements and/or overall progress of the API development within the given timeframe.


### References

- https://fastapi.tiangolo.com/alternatives/?h=inspiration
- https://pixi.sh/latest/vision/
- https://sqldocs.org/sqlite/sqlite-vs-postgresql/
- https://www.pulumi.com/blog/how-a-bank-modernized-its-software-engineering-with-infrastructure-as-code-automation/
- https://fly.io/

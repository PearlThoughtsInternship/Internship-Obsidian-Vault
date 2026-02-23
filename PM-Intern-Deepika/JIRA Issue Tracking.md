We connect Jira with Obsidian so that planning and tracking are not separate activities. Jira tracks execution, while Obsidian supports analysis, decision-making and communication. The integration lets a PM prepare standups, retrospectives, and stakeholder updates using live project data without repeatedly switching tools.

**So Far Analysis:**
-  Getting an overview of the tasks and stories, reducing the hustle behind to search each and every task.
-  Clear status is provided in the obsidian along with the links to navigate through each stories.
-  Effective in time saving and fast status generation.

## IN PROGRESS TASKS

```jira-search
type: table
query: project = SCRUM AND status = "In Progress"
```


## TASKS COMPLETED

```jira-search
type: table
query: project = SCRUM AND status = Done
```



## My Tasks
```jira-search
type: table
query: assignee = "Deepika Kumari" AND status != Done
```

## Current Sprint
```jira-search
type: table
query: project = SCRUM AND sprint in openSprints()
```

## Completed Recently
```jira-search
type: table
query: project = SCRUM AND status = Done ORDER BY updated DESC
```

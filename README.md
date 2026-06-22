# notify-action

Sends a workflow status notification to a matrix room.

## Login and room info

Input: `homeserver`
Input: `access_token`

The homeserver and access token of an account can be found at the bottom of Settings > Help & About in the Element Web client.

Input: `room_id`
The [room id](https://spec.matrix.org/v1.18/appendices/#common-identifier-format) of the room to post in following the format `!string:domain`.
The account needs to be member of the room for this action to work.

## Message format

The message follows the following structure:

```
status_icon [repository/workflow](link) timestamp mention
```

The message is dense to make it easier to view on mobile clients.

## Status

Input: `status`
Default: `job.status`

`status` | `status_icon`
--- | ---
`success` | 🟢
`failure` | 🟥
`skipped` | 🔷

We use different shape to support monochrome output.

## Repository

Input: `repository`
Default: `github.repository`

The owner part `owner/` will be stripped in the output.
 
## Link

Input: `link`
Default: `${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}`

## Mention

Input: `tag_all`
Default: `false`

Mentions all people in the room using `@room`.

## Timestamp

This is the current timestamp in format `DD.MM.YYTHH:MM` in `CET`.

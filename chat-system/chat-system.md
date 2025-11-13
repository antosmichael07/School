```
Enum users.status {
  Online
  Offline
  Idle
  "Do not disturb"
}

Table users {
  id int [pk, increment]
  username varchar(50) [not null]
  email varchar(100) [not null]
  avatar_url text
  created_at datetime
  status users.status

  indexes {
    username [name: "username", unique]
    email [name: "email", unique]
    created_at [name: "created_at"]
    status [name: "status"]
  }
}

Table servers {
  id int [pk, increment]
  name varchar(100) [not null]
  icon_url text
  owner_id int [not null, ref: > users.id]
  created_at datetime

  indexes {
    "name" [name: "name"]
    created_at [name: "created_at"]
  }
}

Table server_members {
  id int [pk, increment]
  user_id int [not null, ref: > users.id]
  server_id int [not null, ref: > servers.id]
  joined_at datetime
  nickname varchar(50)

  indexes {
    joined_at [name: "joined_at"]
    nickname [name: "nickname"]
  }
}

Table roles {
  id int [pk, increment]
  server_id int [not null, ref: > servers.id]
  name varchar(50) [not null]
  color varchar(7)
  permissions text
  position int

  indexes {
    "name" [name: "name"]
    position [name: "position"]
  }
}

Table member_roles {
  id int [pk, increment]
  member_id int [not null, ref: > server_members.id]
  role_id int [not null, ref: > roles.id]
}

Enum channels.type {
  "Text"
  Voice
  Announcement
}

Table channels {
  id int [pk, increment]
  server_id int [not null, ref: > servers.id]
  name varchar(100) [not null]
  type channels.type [not null]
  position int
  created_at datetime

  indexes {
    "name" [name: "name"]
    type [name: "type"]
    position [name: "position"]
    created_at [name: "created_at"]
  }
}

Table messages {
  id int [pk, increment]
  channel_id int [not null, ref: > channels.id]
  author_id int [not null, ref: > users.id]
  content text [not null]
  created_at datetime

  indexes {
    content [name: "content"]
    created_at [name: "created_at"]
  }
}

Table direct_messages {
  id int [pk, increment]
  sender_id int [not null, ref: > users.id]
  receiver_id int [not null, ref: > users.id]
  content text [not null]
  created_at datetime

  indexes {
    content [name: "content"]
    created_at [name: "created_at"]
  }
}

Table reactions {
  id int [pk, increment]
  message_id int [not null, ref: > messages.id]
  user_id int [not null, ref: > users.id]
  emoji varchar(50) [not null]
  created_at datetime

  indexes {
    emoji [name: "emoji"]
    created_at [name: "created_at"]
  }
}

Table invites {
  id int [pk, increment]
  server_id int [not null, ref: > servers.id]
  channel_id int [ref: > channels.id]
  inviter_id int [ref: > users.id]
  expires_at datetime
  max_uses int
  uses int

  indexes {
    expires_at [name: "expires_at"]
    max_uses [name: "max_uses"]
    uses [name: "uses"]
  }
}
```

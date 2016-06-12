BEGIN TRANSACTION;
CREATE TABLE "tweets_tweet" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "tweet_id" varchar(200) NOT NULL, "name" varchar(200) NOT NULL, "date_added" datetime NULL, "date_published" datetime NULL, "text" varchar(200) NOT NULL);
CREATE TABLE "tweets_sourcetwitter" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "tweet_id" integer NOT NULL REFERENCES "tweets_tweet" ("id"), "matched" bool NOT NULL);
CREATE TABLE "tweets_sourcesite" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "url" varchar(2000) NOT NULL, "tweet_id" integer NOT NULL REFERENCES "tweets_tweet" ("id"), "domain" varchar(2000) NOT NULL, "matched" bool NOT NULL);
CREATE TABLE "tweets_keyword" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "tweet_id" integer NOT NULL REFERENCES "tweets_tweet" ("id"), "name" varchar(200) NOT NULL);
CREATE TABLE "tweets_countlog" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "retweet_count" integer unsigned NOT NULL, "favorite_count" integer unsigned NOT NULL, "date" datetime NULL, "tweet_id" integer NOT NULL REFERENCES "tweets_tweet" ("id"));
CREATE TABLE "taggit_taggeditem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" integer NOT NULL, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id"), "tag_id" integer NOT NULL REFERENCES "taggit_tag" ("id"));
CREATE TABLE "taggit_tag" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "slug" varchar(100) NOT NULL UNIQUE);
CREATE TABLE "explorer_sourcetwitteralias" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "alias" varchar(200) NOT NULL UNIQUE, "primary_id" integer NOT NULL REFERENCES "explorer_sourcetwitter" ("id"));
CREATE TABLE "explorer_sourcetwitter" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL UNIQUE);
CREATE TABLE "explorer_sourcesitealias" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "primary_id" integer NOT NULL REFERENCES "explorer_sourcesite" ("id"), "alias" varchar(200) NOT NULL UNIQUE);
CREATE TABLE "explorer_sourcesite" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "url" varchar(2000) NOT NULL UNIQUE, "name" varchar(200) NOT NULL UNIQUE);
CREATE TABLE "explorer_referringtwitter" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL UNIQUE);
CREATE TABLE "explorer_referringsitefilter" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "pattern" varchar(1000) NOT NULL, "site_id" integer NOT NULL REFERENCES "explorer_referringsite" ("id"), "regex" bool NOT NULL);
CREATE TABLE "explorer_referringsitecssselector" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "field" smallint unsigned NOT NULL, "pattern" varchar(1000) NOT NULL, "site_id" integer NOT NULL REFERENCES "explorer_referringsite" ("id"), "regex" varchar(1000) NOT NULL);
CREATE TABLE "explorer_referringsite" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "url" varchar(2000) NOT NULL UNIQUE, "mode" smallint unsigned NOT NULL, "check" bool NOT NULL, "name" varchar(200) NOT NULL UNIQUE);
CREATE TABLE "explorer_keyword" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL UNIQUE);
CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL, UNIQUE ("app_label", "model"));
CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "action_time" datetime NOT NULL, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL, "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id"), "user_id" integer NOT NULL REFERENCES "auth_user" ("id"));
CREATE TABLE "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id"), "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"), UNIQUE ("user_id", "permission_id"));
CREATE TABLE "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id"), "group_id" integer NOT NULL REFERENCES "auth_group" ("id"), UNIQUE ("user_id", "group_id"));
CREATE TABLE "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NOT NULL, "is_superuser" bool NOT NULL, "username" varchar(30) NOT NULL UNIQUE, "first_name" varchar(30) NOT NULL, "last_name" varchar(30) NOT NULL, "email" varchar(75) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL);
CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id"), "codename" varchar(100) NOT NULL, UNIQUE ("content_type_id", "codename"));
CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id"), "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"), UNIQUE ("group_id", "permission_id"));
CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(80) NOT NULL UNIQUE);
CREATE TABLE "articles_version" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "text" text NOT NULL, "language" varchar(200) NOT NULL, "date_added" datetime NULL, "date_last_seen" datetime NULL, "date_published" datetime NULL, "found_by" varchar(100) NOT NULL, "article_id" integer NOT NULL REFERENCES "articles_article" ("id"), "text_hash" varchar(100) NOT NULL UNIQUE);
CREATE TABLE "articles_url" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "article_id" integer NOT NULL REFERENCES "articles_article" ("id"), "name" varchar(2000) NOT NULL UNIQUE);
CREATE TABLE "articles_sourcetwitter" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "matched" bool NOT NULL, "version_id" integer NOT NULL REFERENCES "articles_version" ("id"));
CREATE TABLE "articles_sourcesite" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "url" varchar(2000) NOT NULL, "domain" varchar(2000) NOT NULL, "matched" bool NOT NULL, "local" bool NOT NULL, "anchor_text" varchar(2000) NOT NULL, "version_id" integer NOT NULL REFERENCES "articles_version" ("id"));
CREATE TABLE "articles_keyword" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "version_id" integer NOT NULL REFERENCES "articles_version" ("id"));
CREATE TABLE "articles_author" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "version_id" integer NOT NULL REFERENCES "articles_version" ("id"));
CREATE TABLE "articles_article" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "domain" varchar(2000) NOT NULL);
CREATE TABLE "advanced_filters_advancedfilter_users" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "advancedfilter_id" integer NOT NULL,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    UNIQUE ("advancedfilter_id", "user_id")
);
CREATE TABLE "advanced_filters_advancedfilter_groups" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "advancedfilter_id" integer NOT NULL,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id"),
    UNIQUE ("advancedfilter_id", "group_id")
);
CREATE TABLE "advanced_filters_advancedfilter" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" varchar(255) NOT NULL,
    "created_by_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "url" varchar(255) NOT NULL,
    "b64_query" varchar(2048) NOT NULL,
    "model" varchar(64)
);
CREATE INDEX tweets_sourcetwitter_cea90699 ON "tweets_sourcetwitter" ("tweet_id");
CREATE INDEX tweets_sourcesite_cea90699 ON "tweets_sourcesite" ("tweet_id");
CREATE INDEX tweets_keyword_cea90699 ON "tweets_keyword" ("tweet_id");
CREATE INDEX tweets_countlog_cea90699 ON "tweets_countlog" ("tweet_id");
CREATE INDEX taggit_taggeditem_af31437c ON "taggit_taggeditem" ("object_id");
CREATE INDEX taggit_taggeditem_76f094bc ON "taggit_taggeditem" ("tag_id");
CREATE INDEX taggit_taggeditem_417f1b1c ON "taggit_taggeditem" ("content_type_id");
CREATE INDEX explorer_sourcetwitteralias_095f2624 ON "explorer_sourcetwitteralias" ("primary_id");
CREATE INDEX explorer_sourcesitealias_095f2624 ON "explorer_sourcesitealias" ("primary_id");
CREATE INDEX explorer_referringsitefilter_9365d6e7 ON "explorer_referringsitefilter" ("site_id");
CREATE INDEX explorer_referringsitecssselector_9365d6e7 ON "explorer_referringsitecssselector" ("site_id");
CREATE INDEX django_session_de54fa62 ON "django_session" ("expire_date");
CREATE INDEX django_admin_log_e8701ad4 ON "django_admin_log" ("user_id");
CREATE INDEX django_admin_log_417f1b1c ON "django_admin_log" ("content_type_id");
CREATE INDEX auth_user_user_permissions_e8701ad4 ON "auth_user_user_permissions" ("user_id");
CREATE INDEX auth_user_user_permissions_8373b171 ON "auth_user_user_permissions" ("permission_id");
CREATE INDEX auth_user_groups_e8701ad4 ON "auth_user_groups" ("user_id");
CREATE INDEX auth_user_groups_0e939a4f ON "auth_user_groups" ("group_id");
CREATE INDEX auth_permission_417f1b1c ON "auth_permission" ("content_type_id");
CREATE INDEX auth_group_permissions_8373b171 ON "auth_group_permissions" ("permission_id");
CREATE INDEX auth_group_permissions_0e939a4f ON "auth_group_permissions" ("group_id");
CREATE INDEX articles_version_a00c1b00 ON "articles_version" ("article_id");
CREATE INDEX articles_url_a00c1b00 ON "articles_url" ("article_id");
CREATE INDEX articles_sourcetwitter_316e8552 ON "articles_sourcetwitter" ("version_id");
CREATE INDEX articles_sourcesite_316e8552 ON "articles_sourcesite" ("version_id");
CREATE INDEX articles_keyword_316e8552 ON "articles_keyword" ("version_id");
CREATE INDEX articles_author_316e8552 ON "articles_author" ("version_id");
CREATE INDEX "advanced_filters_advancedfilter_users_f537086c" ON "advanced_filters_advancedfilter_users" ("advancedfilter_id");
CREATE INDEX "advanced_filters_advancedfilter_users_6340c63c" ON "advanced_filters_advancedfilter_users" ("user_id");
CREATE INDEX "advanced_filters_advancedfilter_groups_f537086c" ON "advanced_filters_advancedfilter_groups" ("advancedfilter_id");
CREATE INDEX "advanced_filters_advancedfilter_groups_5f412f9a" ON "advanced_filters_advancedfilter_groups" ("group_id");
CREATE INDEX "advanced_filters_advancedfilter_0c98d849" ON "advanced_filters_advancedfilter" ("created_by_id");
COMMIT;

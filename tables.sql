CREATE TABLE users (
    user_id SERIAL PRIMARY KEY, 
    username TEXT NOT NULL, 
    password TEXT NOT NULL
);

CREATE TABLE admins (
    admin_id SERIAL PRIMARY KEY, 
    user_id INT NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES users (user_id)
);

CREATE TABLE topics (
    topic_id SERIAL PRIMARY KEY,
    header TEXT NOT NULL,
    private_key INT
);

CREATE TABLE privrooms (
    slip_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    private_key INT NOT NULL REFERENCES topics(private_key),
    FOREIGN KEY(user_id)
        REFERENCES users (user_id)
);

CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    topic_id INT NOT NULL,
    owner_id INT NOT NULL,
    header TEXT NOT NULL,
    content TEXT NOT NULL,
    post_time TIMESTAMP,
    FOREIGN KEY (owner_id)
        REFERENCES users (user_id),
    FOREIGN KEY (topic_id)
        REFERENCES topics (topic_id)
);


CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    post_id INT NOT NULL,
    owner_id INT NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP,
    FOREIGN KEY (owner_id)
        REFERENCES users (user_id),
    FOREIGN KEY (post_id)
        REFERENCES posts (post_id)
);
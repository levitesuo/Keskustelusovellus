CREATE TABLE users (
    user_id SERIAL PRIMARY KEY, 
    username TEXT NOT NULL UNIQUE, 
    is_admin BOOLEAN,
    password TEXT NOT NULL
);

CREATE TABLE topics (
    topic_id SERIAL PRIMARY KEY,
    header TEXT NOT NULL,
    owner_id INT NOT NULL,
    timestamp TIMESTAMP,
    private_key INT,
    FOREIGN KEY(owner_id)
        REFERENCES users (user_id)
        ON DELETE CASCADE
);

CREATE TABLE privrooms (
    slip_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    private_key INT NOT NULL,
    FOREIGN KEY(user_id)
        REFERENCES users (user_id)
        ON DELETE CASCADE
);

CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    topic_id INT NOT NULL,
    owner_id INT NOT NULL,
    header TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP,
    FOREIGN KEY (owner_id)
        REFERENCES users (user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (topic_id)
        REFERENCES topics (topic_id)
        ON DELETE CASCADE
);


CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    post_id INT NOT NULL,
    owner_id INT NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP,
    FOREIGN KEY (owner_id)
        REFERENCES users (user_id) 
        ON DELETE CASCADE,
    FOREIGN KEY (post_id)
        REFERENCES posts (post_id) 
        ON DELETE CASCADE
);

INSERT INTO 
    users(username, password, is_admin) 
    VALUES 
    ('admin', 'scrypt:32768:8:1$sRjhMFcFiOBzfkhN$f3dd4c05a2553b139e3caec90198cf10ce13fa7067696d41ceb9975628f3aafa8efeaf23e89dd30b4db637b4c0e10481aa1152dc71404b96585b8930e6a3ab60', TRUE);
    
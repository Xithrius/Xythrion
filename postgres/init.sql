CREATE TABLE link_map(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP DEFAULT now(),
    sid BIGINT NOT NULL,
    uid BIGINT NOT NULL,
    from_match TEXT,
    to_match TEXT
);

INSERT INTO link_map (sid, uid, from_match, to_match) VALUES(
    931030564801245214,
    196664644113268736,
    'https://www.youtube.com/shorts/',
    'https://www.youtube.com/watch?v='
);

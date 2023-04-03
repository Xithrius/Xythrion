CREATE TABLE link_remaps(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP DEFAULT now(),
    sid VARCHAR NOT NULL,
    uid VARCHAR NOT NULL,
    from_match TEXT,
    to_match TEXT
);

INSERT INTO link_remaps (sid, uid, from_match, to_match) VALUES(
    '931030564801245214',
    '196664644113268736',
    'https://www.youtube.com/shorts/',
    'https://www.youtube.com/watch?v='
);

CREATE TABLE web_remaps(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP DEFAULT now(),
    sid VARCHAR NOT NULL,
    uid VARCHAR NOT NULL,
    from_match TEXT,
    xpath TEXT
);

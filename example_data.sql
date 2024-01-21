--
-- PostgreSQL database dump
--

-- Dumped from database version 12.15
-- Dumped by pg_dump version 12.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: comments; Type: TABLE; Schema: public; Owner: leevisuo
--

CREATE TABLE public.comments (
    comment_id integer NOT NULL,
    post_id integer NOT NULL,
    owner_id integer NOT NULL,
    content text NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.comments OWNER TO leevisuo;

--
-- Name: comments_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: leevisuo
--

CREATE SEQUENCE public.comments_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comments_comment_id_seq OWNER TO leevisuo;

--
-- Name: comments_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: leevisuo
--

ALTER SEQUENCE public.comments_comment_id_seq OWNED BY public.comments.comment_id;


--
-- Name: posts; Type: TABLE; Schema: public; Owner: leevisuo
--

CREATE TABLE public.posts (
    post_id integer NOT NULL,
    topic_id integer NOT NULL,
    owner_id integer NOT NULL,
    header text NOT NULL,
    content text NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.posts OWNER TO leevisuo;

--
-- Name: posts_post_id_seq; Type: SEQUENCE; Schema: public; Owner: leevisuo
--

CREATE SEQUENCE public.posts_post_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.posts_post_id_seq OWNER TO leevisuo;

--
-- Name: posts_post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: leevisuo
--

ALTER SEQUENCE public.posts_post_id_seq OWNED BY public.posts.post_id;


--
-- Name: privrooms; Type: TABLE; Schema: public; Owner: leevisuo
--

CREATE TABLE public.privrooms (
    slip_id integer NOT NULL,
    user_id integer NOT NULL,
    private_key integer NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.privrooms OWNER TO leevisuo;

--
-- Name: privrooms_slip_id_seq; Type: SEQUENCE; Schema: public; Owner: leevisuo
--

CREATE SEQUENCE public.privrooms_slip_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.privrooms_slip_id_seq OWNER TO leevisuo;

--
-- Name: privrooms_slip_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: leevisuo
--

ALTER SEQUENCE public.privrooms_slip_id_seq OWNED BY public.privrooms.slip_id;


--
-- Name: topics; Type: TABLE; Schema: public; Owner: leevisuo
--

CREATE TABLE public.topics (
    topic_id integer NOT NULL,
    header text NOT NULL,
    owner_id integer NOT NULL,
    "timestamp" timestamp without time zone,
    private_key integer
);


ALTER TABLE public.topics OWNER TO leevisuo;

--
-- Name: topics_topic_id_seq; Type: SEQUENCE; Schema: public; Owner: leevisuo
--

CREATE SEQUENCE public.topics_topic_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.topics_topic_id_seq OWNER TO leevisuo;

--
-- Name: topics_topic_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: leevisuo
--

ALTER SEQUENCE public.topics_topic_id_seq OWNED BY public.topics.topic_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: leevisuo
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username text NOT NULL,
    is_admin boolean,
    password text NOT NULL
);


ALTER TABLE public.users OWNER TO leevisuo;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: leevisuo
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO leevisuo;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: leevisuo
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: comments comment_id; Type: DEFAULT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.comments ALTER COLUMN comment_id SET DEFAULT nextval('public.comments_comment_id_seq'::regclass);


--
-- Name: posts post_id; Type: DEFAULT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.posts ALTER COLUMN post_id SET DEFAULT nextval('public.posts_post_id_seq'::regclass);


--
-- Name: privrooms slip_id; Type: DEFAULT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.privrooms ALTER COLUMN slip_id SET DEFAULT nextval('public.privrooms_slip_id_seq'::regclass);


--
-- Name: topics topic_id; Type: DEFAULT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.topics ALTER COLUMN topic_id SET DEFAULT nextval('public.topics_topic_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: leevisuo
--

COPY public.comments (comment_id, post_id, owner_id, content, "timestamp") FROM stdin;
1	1	1	Sä oot idiootti.	2024-01-21 20:55:42.172585
2	1	1	Täs on jotain ideaa.	2024-01-21 20:55:48.699311
3	1	1	Oikeesti jep ja sitte Roopesta vois tulla valtiovarainministeri.	2024-01-21 20:56:04.179993
4	1	1	PS <3	2024-01-21 20:56:12.587551
5	2	1	Äitis oli	2024-01-21 20:57:19.629144
6	3	1	Oot väärä. Siilit on parhaita	2024-01-21 20:59:08.838712
7	4	1	Noh oliko nyt kivasti sanottu	2024-01-21 20:59:50.762368
8	6	3	SSSSSSSSSSGGGHHHHHHHH	2024-01-21 21:03:27.262213
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: leevisuo
--

COPY public.posts (post_id, topic_id, owner_id, header, content, "timestamp") FROM stdin;
1	4	1	Aku Ankka pressaks 2024	Musta Aku ois kaikkein paras vaihtoehto. Saatas iha hemosti julkisuutta ulkomailta ja saatais jotain kilpailua tolle USA:n donald meiningille. Mä en ymmärrä miks porukka ei puhu tästä enempää.	2024-01-21 20:55:27.344967
2	4	1	Politiikka on tyhmää	Kaikki politiikka on iha tyhmää, ne poliitikot on tyhmiä, äänestäjät on tyhmiä ja te ootte tyhmiä ku juttelette asiasta. Iha typerää kaikki ja sekä koko juttu.	2024-01-21 20:57:09.043988
3	3	1	Laiskiaiset apriciation post	Laiskiaiset on ehdottomasti paras eiläin. Niitten päällä legit elää jotain naavaa jota ne sit safkaa ja saa siit elintärkeitä kivennäisaineita. Niitte kylkiluut on kehittyny sillai et vaik ne tipahtais jostain 100000 m puunlatvasta ne vaa pomppii ku joku pallo.	2024-01-21 20:58:56.567928
4	3	1	Mursu on eläinkunnan lappeenranta	Emt. Tykkäävät vedestä tai jotain.	2024-01-21 20:59:42.356318
5	2	1	Tää kanava on kuoll	Kukaan ei oo koskaan jutellu täällä mistään. Miks tämmösii kavania edes luodaan. Iha sairaan typerää.	2024-01-21 21:00:32.970263
6	5	3	Shhshshhshsh	ssshshhshhshshs shshs shshssshs hsh shshshs	2024-01-21 21:03:19.380082
7	5	2	Sheesh	SHSHSHSHSHSHSHSHSHSHHSH	2024-01-21 21:12:49.017265
8	2	2	Mun lempi elokuva on kanala_lakana_kalana	Tykkään kanoista ja kaloista, mutta lakanat ei oikee nappaa. Siitä huolimatta tämä elokuva kutkuttaa mua joka kerta ku katon sen.\r\n	2024-01-21 21:35:15.856369
9	6	4	Feels like this could be forever right now, don't wanna sleep cause we're dreaming out loud.	From "A.M." off Made in the A.M. Doesn't everyone long to be in a situation, whether it's a relationship or chapter of your life, that is so incredible it feels like a dream? Maybe you've even felt this way while at a 1D concert in the past--guilty as charged.\r\n\r\n	2024-01-21 21:36:31.266939
\.


--
-- Data for Name: privrooms; Type: TABLE DATA; Schema: public; Owner: leevisuo
--

COPY public.privrooms (slip_id, user_id, private_key, "timestamp") FROM stdin;
1	2	5	2024-01-21 21:01:51.636301
2	3	5	2024-01-21 21:02:54.428747
3	4	6	2024-01-21 21:11:55.779018
4	3	6	2024-01-21 21:12:01.013832
\.


--
-- Data for Name: topics; Type: TABLE DATA; Schema: public; Owner: leevisuo
--

COPY public.topics (topic_id, header, owner_id, "timestamp", private_key) FROM stdin;
1	Musiikki	1	2024-01-21 20:51:33.85671	\N
2	Elokuvat	1	2024-01-21 20:51:40.223859	\N
3	Eläimet	1	2024-01-21 20:51:43.99263	\N
4	Politiikka	1	2024-01-21 20:51:48.94996	\N
5	Salaisuuksien kammio	1	2024-01-21 21:01:05.684733	5
6	One direction	1	2024-01-21 21:11:48.760373	6
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: leevisuo
--

COPY public.users (user_id, username, is_admin, password) FROM stdin;
1	admin	t	scrypt:32768:8:1$sRjhMFcFiOBzfkhN$f3dd4c05a2553b139e3caec90198cf10ce13fa7067696d41ceb9975628f3aafa8efeaf23e89dd30b4db637b4c0e10481aa1152dc71404b96585b8930e6a3ab60
2	Käärme	\N	scrypt:32768:8:1$ipRFayZWZmvVAQol$ef7faad4327f9229c4db7e7e2b83ccb0871adb04603e82f5ae6297f320e4b2528b951ff3b6de8394839fd1828aa791e62354b1609165bbe16e55d1194fe82a9b
3	Harry	\N	scrypt:32768:8:1$6JOJWderLhHXs3YH$f7c2e3d3d34da2d28bc29689a402a9722cbcb56cdd94ab46fb50b11bab2057e915866be84bc07693816f805d3c407b68268c7d2bc4f7f83ffd6f965a8377035c
4	Zayn	\N	scrypt:32768:8:1$RQaVQCT8V31WzgPK$c5e2fdb8eaceaaa34fef5e5c91e24cec222175839a119b681cb38ed733b95dc1e2b096b3d77065697eb2d2bc40b0387403631d5fafb7ac0132b96656e8de572d
\.


--
-- Name: comments_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leevisuo
--

SELECT pg_catalog.setval('public.comments_comment_id_seq', 8, true);


--
-- Name: posts_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leevisuo
--

SELECT pg_catalog.setval('public.posts_post_id_seq', 9, true);


--
-- Name: privrooms_slip_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leevisuo
--

SELECT pg_catalog.setval('public.privrooms_slip_id_seq', 4, true);


--
-- Name: topics_topic_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leevisuo
--

SELECT pg_catalog.setval('public.topics_topic_id_seq', 6, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leevisuo
--

SELECT pg_catalog.setval('public.users_user_id_seq', 4, true);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (comment_id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (post_id);


--
-- Name: privrooms privrooms_pkey; Type: CONSTRAINT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.privrooms
    ADD CONSTRAINT privrooms_pkey PRIMARY KEY (slip_id);


--
-- Name: topics topics_pkey; Type: CONSTRAINT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.topics
    ADD CONSTRAINT topics_pkey PRIMARY KEY (topic_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: comments comments_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: comments comments_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(post_id) ON DELETE CASCADE;


--
-- Name: posts posts_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: posts posts_topic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES public.topics(topic_id) ON DELETE CASCADE;


--
-- Name: privrooms privrooms_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.privrooms
    ADD CONSTRAINT privrooms_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: topics topics_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: leevisuo
--

ALTER TABLE ONLY public.topics
    ADD CONSTRAINT topics_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--


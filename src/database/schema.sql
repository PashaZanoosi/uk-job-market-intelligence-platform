--
-- PostgreSQL database dump
--

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

-- Started on 2026-07-20 02:06:10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 227 (class 1259 OID 16453)
-- Name: job_skills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_skills (
    job_id character varying(50) NOT NULL,
    skill_id integer NOT NULL,
    confidence_score double precision,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 236 (class 1259 OID 16557)
-- Name: job_skills_backup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_skills_backup (
    job_id character varying(50),
    skill_id integer,
    confidence_score double precision,
    created_at timestamp without time zone
);


--
-- TOC entry 224 (class 1259 OID 16418)
-- Name: job_snapshots; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_snapshots (
    snapshot_id integer NOT NULL,
    job_id character varying(50),
    snapshot_date date,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 223 (class 1259 OID 16417)
-- Name: job_snapshots_snapshot_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.job_snapshots_snapshot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- TOC entry 5110 (class 0 OID 0)
-- Dependencies: 223
-- Name: job_snapshots_snapshot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.job_snapshots_snapshot_id_seq OWNED BY public.job_snapshots.snapshot_id;


--
-- TOC entry 219 (class 1259 OID 16397)
-- Name: jobs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jobs (
    job_id character varying(50) NOT NULL,
    title text,
    company text,
    location text,
    salary_min integer,
    salary_max integer,
    average_salary integer,
    created_date date,
    description text,
    category text
);


--
-- TOC entry 233 (class 1259 OID 16519)
-- Name: skill_demand_snapshots; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skill_demand_snapshots (
    snapshot_id integer NOT NULL,
    snapshot_date date NOT NULL,
    skill_id integer NOT NULL,
    job_count integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 232 (class 1259 OID 16518)
-- Name: skill_demand_snapshots_snapshot_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.skill_demand_snapshots_snapshot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5111 (class 0 OID 0)
-- Dependencies: 232
-- Name: skill_demand_snapshots_snapshot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.skill_demand_snapshots_snapshot_id_seq OWNED BY public.skill_demand_snapshots.snapshot_id;


--
-- TOC entry 229 (class 1259 OID 16478)
-- Name: skill_taxonomy; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skill_taxonomy (
    taxonomy_id integer NOT NULL,
    parent_id integer,
    name character varying(255) NOT NULL,
    level integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 231 (class 1259 OID 16499)
-- Name: skill_taxonomy_suggestions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skill_taxonomy_suggestions (
    suggestion_id integer NOT NULL,
    skill_id integer,
    suggested_taxonomy_id integer,
    confidence_score double precision,
    source character varying(50),
    status character varying(20) DEFAULT 'pending'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 230 (class 1259 OID 16498)
-- Name: skill_taxonomy_suggestions_suggestion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.skill_taxonomy_suggestions_suggestion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5112 (class 0 OID 0)
-- Dependencies: 230
-- Name: skill_taxonomy_suggestions_suggestion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.skill_taxonomy_suggestions_suggestion_id_seq OWNED BY public.skill_taxonomy_suggestions.suggestion_id;


--
-- TOC entry 228 (class 1259 OID 16477)
-- Name: skill_taxonomy_taxonomy_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.skill_taxonomy_taxonomy_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5113 (class 0 OID 0)
-- Dependencies: 228
-- Name: skill_taxonomy_taxonomy_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.skill_taxonomy_taxonomy_id_seq OWNED BY public.skill_taxonomy.taxonomy_id;


--
-- TOC entry 226 (class 1259 OID 16427)
-- Name: skills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skills (
    skill_id integer NOT NULL,
    skill_name character varying(100),
    category character varying(50),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    taxonomy_id integer
);


--
-- TOC entry 237 (class 1259 OID 16560)
-- Name: skills_backup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skills_backup (
    skill_id integer,
    skill_name character varying(100),
    category character varying(50),
    created_at timestamp without time zone,
    taxonomy_id integer
);


--
-- TOC entry 225 (class 1259 OID 16426)
-- Name: skills_skill_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.skills_skill_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5114 (class 0 OID 0)
-- Dependencies: 225
-- Name: skills_skill_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.skills_skill_id_seq OWNED BY public.skills.skill_id;


--
-- TOC entry 235 (class 1259 OID 16536)
-- Name: taxonomy_demand_snapshots; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.taxonomy_demand_snapshots (
    snapshot_id integer NOT NULL,
    snapshot_date date NOT NULL,
    taxonomy_id integer NOT NULL,
    job_count integer NOT NULL,
    skill_count integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 234 (class 1259 OID 16535)
-- Name: taxonomy_demand_snapshots_snapshot_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.taxonomy_demand_snapshots_snapshot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5115 (class 0 OID 0)
-- Dependencies: 234
-- Name: taxonomy_demand_snapshots_snapshot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.taxonomy_demand_snapshots_snapshot_id_seq OWNED BY public.taxonomy_demand_snapshots.snapshot_id;


--
-- TOC entry 220 (class 1259 OID 16405)
-- Name: vw_jobs_by_location; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vw_jobs_by_location AS
 SELECT location,
    count(*) AS total_jobs
   FROM public.jobs
  GROUP BY location
  ORDER BY (count(*)) DESC;


--
-- TOC entry 221 (class 1259 OID 16409)
-- Name: vw_salary_analysis; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vw_salary_analysis AS
 SELECT title,
    count(*) AS job_count,
    round(avg(average_salary), 0) AS average_salary
   FROM public.jobs
  WHERE (average_salary IS NOT NULL)
  GROUP BY title
  ORDER BY (round(avg(average_salary), 0)) DESC;


--
-- TOC entry 222 (class 1259 OID 16413)
-- Name: vw_top_hiring_companies; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vw_top_hiring_companies AS
 SELECT company,
    count(*) AS vacancies
   FROM public.jobs
  GROUP BY company
  ORDER BY (count(*)) DESC
 LIMIT 20;


--
-- TOC entry 4909 (class 2604 OID 16421)
-- Name: job_snapshots snapshot_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_snapshots ALTER COLUMN snapshot_id SET DEFAULT nextval('public.job_snapshots_snapshot_id_seq'::regclass);


--
-- TOC entry 4919 (class 2604 OID 16522)
-- Name: skill_demand_snapshots snapshot_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_demand_snapshots ALTER COLUMN snapshot_id SET DEFAULT nextval('public.skill_demand_snapshots_snapshot_id_seq'::regclass);


--
-- TOC entry 4914 (class 2604 OID 16481)
-- Name: skill_taxonomy taxonomy_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_taxonomy ALTER COLUMN taxonomy_id SET DEFAULT nextval('public.skill_taxonomy_taxonomy_id_seq'::regclass);


--
-- TOC entry 4916 (class 2604 OID 16502)
-- Name: skill_taxonomy_suggestions suggestion_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_taxonomy_suggestions ALTER COLUMN suggestion_id SET DEFAULT nextval('public.skill_taxonomy_suggestions_suggestion_id_seq'::regclass);


--
-- TOC entry 4911 (class 2604 OID 16430)
-- Name: skills skill_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skills ALTER COLUMN skill_id SET DEFAULT nextval('public.skills_skill_id_seq'::regclass);


--
-- TOC entry 4921 (class 2604 OID 16539)
-- Name: taxonomy_demand_snapshots snapshot_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxonomy_demand_snapshots ALTER COLUMN snapshot_id SET DEFAULT nextval('public.taxonomy_demand_snapshots_snapshot_id_seq'::regclass);


--
-- TOC entry 4934 (class 2606 OID 16460)
-- Name: job_skills job_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_skills
    ADD CONSTRAINT job_skills_pkey PRIMARY KEY (job_id, skill_id);


--
-- TOC entry 4926 (class 2606 OID 16425)
-- Name: job_snapshots job_snapshots_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_snapshots
    ADD CONSTRAINT job_snapshots_pkey PRIMARY KEY (snapshot_id);


--
-- TOC entry 4924 (class 2606 OID 16404)
-- Name: jobs jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (job_id);


--
-- TOC entry 4940 (class 2606 OID 16529)
-- Name: skill_demand_snapshots skill_demand_snapshots_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_demand_snapshots
    ADD CONSTRAINT skill_demand_snapshots_pkey PRIMARY KEY (snapshot_id);


--
-- TOC entry 4936 (class 2606 OID 16487)
-- Name: skill_taxonomy skill_taxonomy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_taxonomy
    ADD CONSTRAINT skill_taxonomy_pkey PRIMARY KEY (taxonomy_id);


--
-- TOC entry 4938 (class 2606 OID 16507)
-- Name: skill_taxonomy_suggestions skill_taxonomy_suggestions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_taxonomy_suggestions
    ADD CONSTRAINT skill_taxonomy_suggestions_pkey PRIMARY KEY (suggestion_id);


--
-- TOC entry 4930 (class 2606 OID 16434)
-- Name: skills skills_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_pkey PRIMARY KEY (skill_id);


--
-- TOC entry 4932 (class 2606 OID 16436)
-- Name: skills skills_skill_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_skill_name_key UNIQUE (skill_name);


--
-- TOC entry 4944 (class 2606 OID 16547)
-- Name: taxonomy_demand_snapshots taxonomy_demand_snapshots_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxonomy_demand_snapshots
    ADD CONSTRAINT taxonomy_demand_snapshots_pkey PRIMARY KEY (snapshot_id);


--
-- TOC entry 4928 (class 2606 OID 16608)
-- Name: job_snapshots unique_job_snapshot_date; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_snapshots
    ADD CONSTRAINT unique_job_snapshot_date UNIQUE (job_id, snapshot_date);


--
-- TOC entry 4942 (class 2606 OID 16554)
-- Name: skill_demand_snapshots unique_skill_daily_snapshot; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_demand_snapshots
    ADD CONSTRAINT unique_skill_daily_snapshot UNIQUE (snapshot_date, skill_id);


--
-- TOC entry 4946 (class 2606 OID 16556)
-- Name: taxonomy_demand_snapshots unique_taxonomy_daily_snapshot; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxonomy_demand_snapshots
    ADD CONSTRAINT unique_taxonomy_daily_snapshot UNIQUE (snapshot_date, taxonomy_id);


--
-- TOC entry 4953 (class 2606 OID 16530)
-- Name: skill_demand_snapshots fk_skill_snapshot_skill; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_demand_snapshots
    ADD CONSTRAINT fk_skill_snapshot_skill FOREIGN KEY (skill_id) REFERENCES public.skills(skill_id);


--
-- TOC entry 4954 (class 2606 OID 16548)
-- Name: taxonomy_demand_snapshots fk_taxonomy_snapshot_taxonomy; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxonomy_demand_snapshots
    ADD CONSTRAINT fk_taxonomy_snapshot_taxonomy FOREIGN KEY (taxonomy_id) REFERENCES public.skill_taxonomy(taxonomy_id);


--
-- TOC entry 4948 (class 2606 OID 16461)
-- Name: job_skills job_skills_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_skills
    ADD CONSTRAINT job_skills_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(job_id);


--
-- TOC entry 4949 (class 2606 OID 16466)
-- Name: job_skills job_skills_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_skills
    ADD CONSTRAINT job_skills_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(skill_id);


--
-- TOC entry 4950 (class 2606 OID 16488)
-- Name: skill_taxonomy skill_taxonomy_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_taxonomy
    ADD CONSTRAINT skill_taxonomy_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.skill_taxonomy(taxonomy_id);


--
-- TOC entry 4951 (class 2606 OID 16508)
-- Name: skill_taxonomy_suggestions skill_taxonomy_suggestions_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_taxonomy_suggestions
    ADD CONSTRAINT skill_taxonomy_suggestions_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(skill_id);


--
-- TOC entry 4952 (class 2606 OID 16513)
-- Name: skill_taxonomy_suggestions skill_taxonomy_suggestions_suggested_taxonomy_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_taxonomy_suggestions
    ADD CONSTRAINT skill_taxonomy_suggestions_suggested_taxonomy_id_fkey FOREIGN KEY (suggested_taxonomy_id) REFERENCES public.skill_taxonomy(taxonomy_id);


--
-- TOC entry 4947 (class 2606 OID 16493)
-- Name: skills skills_taxonomy_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_taxonomy_id_fkey FOREIGN KEY (taxonomy_id) REFERENCES public.skill_taxonomy(taxonomy_id);


-- Completed on 2026-07-20 02:06:10

--
-- PostgreSQL database dump complete
--


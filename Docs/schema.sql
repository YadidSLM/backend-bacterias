--
-- PostgreSQL database dump
--

-- Dumped from database version 12.22 (Ubuntu 12.22-0ubuntu0.20.04.4)
-- Dumped by pg_dump version 12.22 (Ubuntu 12.22-0ubuntu0.20.04.4)

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
-- Name: arista; Type: TABLE; Schema: public; Owner: bacterias_user
--

CREATE TABLE public.arista (
    id_arista integer NOT NULL,
    id_from_node integer NOT NULL,
    id_to_node integer NOT NULL,
    weight double precision
);


ALTER TABLE public.arista OWNER TO bacterias_user;

--
-- Name: arista_id_arista_seq; Type: SEQUENCE; Schema: public; Owner: bacterias_user
--

CREATE SEQUENCE public.arista_id_arista_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.arista_id_arista_seq OWNER TO bacterias_user;

--
-- Name: arista_id_arista_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bacterias_user
--

ALTER SEQUENCE public.arista_id_arista_seq OWNED BY public.arista.id_arista;


--
-- Name: bacteria; Type: TABLE; Schema: public; Owner: bacterias_user
--

CREATE TABLE public.bacteria (
    id_bacteria integer NOT NULL,
    bacteria character varying(20) NOT NULL
);


ALTER TABLE public.bacteria OWNER TO bacterias_user;

--
-- Name: bacteria_id_bacteria_seq; Type: SEQUENCE; Schema: public; Owner: bacterias_user
--

CREATE SEQUENCE public.bacteria_id_bacteria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bacteria_id_bacteria_seq OWNER TO bacterias_user;

--
-- Name: bacteria_id_bacteria_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bacterias_user
--

ALTER SEQUENCE public.bacteria_id_bacteria_seq OWNED BY public.bacteria.id_bacteria;


--
-- Name: coexp_modulo; Type: TABLE; Schema: public; Owner: bacterias_user
--

CREATE TABLE public.coexp_modulo (
    id_coexp_modulo integer NOT NULL,
    nombre_modulo character varying(30) NOT NULL
);


ALTER TABLE public.coexp_modulo OWNER TO bacterias_user;

--
-- Name: coexp_modulo_id_coexp_modulo_seq; Type: SEQUENCE; Schema: public; Owner: bacterias_user
--

CREATE SEQUENCE public.coexp_modulo_id_coexp_modulo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.coexp_modulo_id_coexp_modulo_seq OWNER TO bacterias_user;

--
-- Name: coexp_modulo_id_coexp_modulo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bacterias_user
--

ALTER SEQUENCE public.coexp_modulo_id_coexp_modulo_seq OWNED BY public.coexp_modulo.id_coexp_modulo;


--
-- Name: expresion; Type: TABLE; Schema: public; Owner: bacterias_user
--

CREATE TABLE public.expresion (
    id_gen integer NOT NULL,
    id_muestra integer NOT NULL,
    expresion double precision NOT NULL
);


ALTER TABLE public.expresion OWNER TO bacterias_user;

--
-- Name: gen; Type: TABLE; Schema: public; Owner: bacterias_user
--

CREATE TABLE public.gen (
    id_gen integer NOT NULL,
    locus_tag character varying(20) NOT NULL,
    id_bacteria integer
);


ALTER TABLE public.gen OWNER TO bacterias_user;

--
-- Name: gen_id_gen_seq; Type: SEQUENCE; Schema: public; Owner: bacterias_user
--

CREATE SEQUENCE public.gen_id_gen_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gen_id_gen_seq OWNER TO bacterias_user;

--
-- Name: gen_id_gen_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bacterias_user
--

ALTER SEQUENCE public.gen_id_gen_seq OWNED BY public.gen.id_gen;


--
-- Name: nodo; Type: TABLE; Schema: public; Owner: bacterias_user
--

CREATE TABLE public.nodo (
    id_nodo integer NOT NULL,
    id_gen integer NOT NULL,
    id_coexp_modulo integer NOT NULL
);


ALTER TABLE public.nodo OWNER TO bacterias_user;

--
-- Name: nodo_id_nodo_seq; Type: SEQUENCE; Schema: public; Owner: bacterias_user
--

CREATE SEQUENCE public.nodo_id_nodo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nodo_id_nodo_seq OWNER TO bacterias_user;

--
-- Name: nodo_id_nodo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bacterias_user
--

ALTER SEQUENCE public.nodo_id_nodo_seq OWNED BY public.nodo.id_nodo;


--
-- Name: arista id_arista; Type: DEFAULT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.arista ALTER COLUMN id_arista SET DEFAULT nextval('public.arista_id_arista_seq'::regclass);


--
-- Name: bacteria id_bacteria; Type: DEFAULT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.bacteria ALTER COLUMN id_bacteria SET DEFAULT nextval('public.bacteria_id_bacteria_seq'::regclass);


--
-- Name: coexp_modulo id_coexp_modulo; Type: DEFAULT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.coexp_modulo ALTER COLUMN id_coexp_modulo SET DEFAULT nextval('public.coexp_modulo_id_coexp_modulo_seq'::regclass);


--
-- Name: gen id_gen; Type: DEFAULT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.gen ALTER COLUMN id_gen SET DEFAULT nextval('public.gen_id_gen_seq'::regclass);


--
-- Name: nodo id_nodo; Type: DEFAULT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.nodo ALTER COLUMN id_nodo SET DEFAULT nextval('public.nodo_id_nodo_seq'::regclass);


--
-- Name: arista arista_pkey; Type: CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.arista
    ADD CONSTRAINT arista_pkey PRIMARY KEY (id_arista);


--
-- Name: bacteria bacteria_bacteria_key; Type: CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.bacteria
    ADD CONSTRAINT bacteria_bacteria_key UNIQUE (bacteria);


--
-- Name: bacteria bacteria_pkey; Type: CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.bacteria
    ADD CONSTRAINT bacteria_pkey PRIMARY KEY (id_bacteria);


--
-- Name: coexp_modulo coexp_modulo_nombre_modulo_key; Type: CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.coexp_modulo
    ADD CONSTRAINT coexp_modulo_nombre_modulo_key UNIQUE (nombre_modulo);


--
-- Name: coexp_modulo coexp_modulo_pkey; Type: CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.coexp_modulo
    ADD CONSTRAINT coexp_modulo_pkey PRIMARY KEY (id_coexp_modulo);


--
-- Name: expresion expresion_pkey; Type: CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.expresion
    ADD CONSTRAINT expresion_pkey PRIMARY KEY (id_gen, id_muestra);


--
-- Name: gen gen_locus_tag_key; Type: CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.gen
    ADD CONSTRAINT gen_locus_tag_key UNIQUE (locus_tag);


--
-- Name: gen gen_pkey; Type: CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.gen
    ADD CONSTRAINT gen_pkey PRIMARY KEY (id_gen);


--
-- Name: nodo nodo_pkey; Type: CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.nodo
    ADD CONSTRAINT nodo_pkey PRIMARY KEY (id_nodo);


--
-- Name: nodo unico_gen_modulo; Type: CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.nodo
    ADD CONSTRAINT unico_gen_modulo UNIQUE (id_gen, id_coexp_modulo);


--
-- Name: arista arista_id_from_node_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.arista
    ADD CONSTRAINT arista_id_from_node_fkey FOREIGN KEY (id_from_node) REFERENCES public.nodo(id_nodo);


--
-- Name: arista arista_id_to_node_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.arista
    ADD CONSTRAINT arista_id_to_node_fkey FOREIGN KEY (id_to_node) REFERENCES public.nodo(id_nodo);


--
-- Name: expresion expresion_id_gen_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.expresion
    ADD CONSTRAINT expresion_id_gen_fkey FOREIGN KEY (id_gen) REFERENCES public.gen(id_gen);


--
-- Name: gen gen_id_bacteria_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.gen
    ADD CONSTRAINT gen_id_bacteria_fkey FOREIGN KEY (id_bacteria) REFERENCES public.bacteria(id_bacteria);


--
-- Name: nodo nodo_id_coexp_modulo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.nodo
    ADD CONSTRAINT nodo_id_coexp_modulo_fkey FOREIGN KEY (id_coexp_modulo) REFERENCES public.coexp_modulo(id_coexp_modulo);


--
-- Name: nodo nodo_id_gen_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bacterias_user
--

ALTER TABLE ONLY public.nodo
    ADD CONSTRAINT nodo_id_gen_fkey FOREIGN KEY (id_gen) REFERENCES public.gen(id_gen);


--
-- PostgreSQL database dump complete
--


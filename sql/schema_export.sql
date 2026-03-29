--
-- PostgreSQL database dump
--

\restrict V4nbd00p7DGcJjrn3dmSVNeOjG5XVv0ONhGmudC0S3GKLM4dLOjDZUubpg8i3Ot

-- Dumped from database version 15.17 (Debian 15.17-1.pgdg13+1)
-- Dumped by pg_dump version 15.17 (Debian 15.17-1.pgdg13+1)

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
-- Name: po_items; Type: TABLE; Schema: public; Owner: po_user
--

CREATE TABLE public.po_items (
    id integer NOT NULL,
    po_id integer NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    unit_price numeric(10,2) NOT NULL,
    line_total numeric(10,2) NOT NULL,
    CONSTRAINT po_items_quantity_check CHECK ((quantity > 0))
);


ALTER TABLE public.po_items OWNER TO po_user;

--
-- Name: po_items_id_seq; Type: SEQUENCE; Schema: public; Owner: po_user
--

CREATE SEQUENCE public.po_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.po_items_id_seq OWNER TO po_user;

--
-- Name: po_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: po_user
--

ALTER SEQUENCE public.po_items_id_seq OWNED BY public.po_items.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: po_user
--

CREATE TABLE public.products (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    sku character varying(100) NOT NULL,
    unit_price numeric(10,2) NOT NULL,
    stock_level integer DEFAULT 0 NOT NULL,
    category character varying(100),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT products_stock_level_check CHECK ((stock_level >= 0)),
    CONSTRAINT products_unit_price_check CHECK ((unit_price >= (0)::numeric))
);


ALTER TABLE public.products OWNER TO po_user;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: po_user
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_id_seq OWNER TO po_user;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: po_user
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: purchase_orders; Type: TABLE; Schema: public; Owner: po_user
--

CREATE TABLE public.purchase_orders (
    id integer NOT NULL,
    reference_no character varying(50) NOT NULL,
    vendor_id integer NOT NULL,
    subtotal numeric(10,2) DEFAULT 0 NOT NULL,
    tax_amount numeric(10,2) DEFAULT 0 NOT NULL,
    total_amount numeric(10,2) DEFAULT 0 NOT NULL,
    status character varying(50) DEFAULT 'Draft'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT purchase_orders_status_check CHECK (((status)::text = ANY ((ARRAY['Draft'::character varying, 'Confirmed'::character varying, 'Received'::character varying, 'Cancelled'::character varying])::text[])))
);


ALTER TABLE public.purchase_orders OWNER TO po_user;

--
-- Name: purchase_orders_id_seq; Type: SEQUENCE; Schema: public; Owner: po_user
--

CREATE SEQUENCE public.purchase_orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.purchase_orders_id_seq OWNER TO po_user;

--
-- Name: purchase_orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: po_user
--

ALTER SEQUENCE public.purchase_orders_id_seq OWNED BY public.purchase_orders.id;


--
-- Name: vendors; Type: TABLE; Schema: public; Owner: po_user
--

CREATE TABLE public.vendors (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    contact character varying(255) NOT NULL,
    rating numeric(2,1),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT vendors_rating_check CHECK (((rating >= (0)::numeric) AND (rating <= (5)::numeric)))
);


ALTER TABLE public.vendors OWNER TO po_user;

--
-- Name: vendors_id_seq; Type: SEQUENCE; Schema: public; Owner: po_user
--

CREATE SEQUENCE public.vendors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.vendors_id_seq OWNER TO po_user;

--
-- Name: vendors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: po_user
--

ALTER SEQUENCE public.vendors_id_seq OWNED BY public.vendors.id;


--
-- Name: po_items id; Type: DEFAULT; Schema: public; Owner: po_user
--

ALTER TABLE ONLY public.po_items ALTER COLUMN id SET DEFAULT nextval('public.po_items_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: po_user
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: purchase_orders id; Type: DEFAULT; Schema: public; Owner: po_user
--

ALTER TABLE ONLY public.purchase_orders ALTER COLUMN id SET DEFAULT nextval('public.purchase_orders_id_seq'::regclass);


--
-- Name: vendors id; Type: DEFAULT; Schema: public; Owner: po_user
--

ALTER TABLE ONLY public.vendors ALTER COLUMN id SET DEFAULT nextval('public.vendors_id_seq'::regclass);


--
-- Name: po_items po_items_pkey; Type: CONSTRAINT; Schema: public; Owner: po_user
--

ALTER TABLE ONLY public.po_items
    ADD CONSTRAINT po_items_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: po_user
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: products products_sku_key; Type: CONSTRAINT; Schema: public; Owner: po_user
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_sku_key UNIQUE (sku);


--
-- Name: purchase_orders purchase_orders_pkey; Type: CONSTRAINT; Schema: public; Owner: po_user
--

ALTER TABLE ONLY public.purchase_orders
    ADD CONSTRAINT purchase_orders_pkey PRIMARY KEY (id);


--
-- Name: purchase_orders purchase_orders_reference_no_key; Type: CONSTRAINT; Schema: public; Owner: po_user
--

ALTER TABLE ONLY public.purchase_orders
    ADD CONSTRAINT purchase_orders_reference_no_key UNIQUE (reference_no);


--
-- Name: vendors vendors_pkey; Type: CONSTRAINT; Schema: public; Owner: po_user
--

ALTER TABLE ONLY public.vendors
    ADD CONSTRAINT vendors_pkey PRIMARY KEY (id);


--
-- Name: po_items po_items_po_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: po_user
--

ALTER TABLE ONLY public.po_items
    ADD CONSTRAINT po_items_po_id_fkey FOREIGN KEY (po_id) REFERENCES public.purchase_orders(id) ON DELETE CASCADE;


--
-- Name: po_items po_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: po_user
--

ALTER TABLE ONLY public.po_items
    ADD CONSTRAINT po_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE RESTRICT;


--
-- Name: purchase_orders purchase_orders_vendor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: po_user
--

ALTER TABLE ONLY public.purchase_orders
    ADD CONSTRAINT purchase_orders_vendor_id_fkey FOREIGN KEY (vendor_id) REFERENCES public.vendors(id) ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

\unrestrict V4nbd00p7DGcJjrn3dmSVNeOjG5XVv0ONhGmudC0S3GKLM4dLOjDZUubpg8i3Ot


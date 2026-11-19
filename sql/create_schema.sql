--
-- PostgreSQL database dump
--

\restrict S4HZn5M9DiiXqQggC0WztfG7sg5Ms7IgMIeEoasSa18rRZTGkdeA3A5x6YawWys

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

-- Started on 2026-11-19 11:08:28

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

SET default_table_access_method = heap;

--
-- TOC entry 223 (class 1259 OID 16524)
-- Name: benefit_plans; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.benefit_plans (
    plan_id integer NOT NULL,
    plan_type character varying(50) NOT NULL
);


--
-- TOC entry 222 (class 1259 OID 16523)
-- Name: benefit_plans_plan_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.benefit_plans ALTER COLUMN plan_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.benefit_plans_plan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 220 (class 1259 OID 16501)
-- Name: departments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.departments (
    department_id integer NOT NULL,
    department_name character varying(100) NOT NULL
);


--
-- TOC entry 219 (class 1259 OID 16500)
-- Name: departments_department_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.departments ALTER COLUMN department_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.departments_department_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 221 (class 1259 OID 16510)
-- Name: employees; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employees (
    employee_id integer NOT NULL,
    employee_name character varying(150) NOT NULL,
    department_id integer NOT NULL
);


--
-- TOC entry 225 (class 1259 OID 16534)
-- Name: enrollments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.enrollments (
    enrollment_id integer NOT NULL,
    employee_id integer NOT NULL,
    plan_id integer NOT NULL,
    monthly_premium numeric(10,2) NOT NULL,
    employee_monthly_cost numeric(10,2) NOT NULL,
    source_enrollment_id character varying(50) NOT NULL,
    effective_date date NOT NULL,
    CONSTRAINT chk_employee_monthly_cost CHECK ((employee_monthly_cost >= (0)::numeric)),
    CONSTRAINT chk_monthly_premium CHECK ((monthly_premium >= (0)::numeric))
);


--
-- TOC entry 224 (class 1259 OID 16533)
-- Name: enrollments_enrollment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.enrollments ALTER COLUMN enrollment_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.enrollments_enrollment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 4879 (class 2606 OID 16530)
-- Name: benefit_plans benefit_plans_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.benefit_plans
    ADD CONSTRAINT benefit_plans_pkey PRIMARY KEY (plan_id);


--
-- TOC entry 4881 (class 2606 OID 16532)
-- Name: benefit_plans benefit_plans_plan_type_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.benefit_plans
    ADD CONSTRAINT benefit_plans_plan_type_key UNIQUE (plan_type);


--
-- TOC entry 4873 (class 2606 OID 16509)
-- Name: departments departments_department_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_department_name_key UNIQUE (department_name);


--
-- TOC entry 4875 (class 2606 OID 16507)
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (department_id);


--
-- TOC entry 4877 (class 2606 OID 16517)
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (employee_id);


--
-- TOC entry 4883 (class 2606 OID 16545)
-- Name: enrollments enrollments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_pkey PRIMARY KEY (enrollment_id);


--
-- TOC entry 4885 (class 2606 OID 16547)
-- Name: enrollments uq_employee_plan; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT uq_employee_plan UNIQUE (employee_id, plan_id);


--
-- TOC entry 4887 (class 2606 OID 16561)
-- Name: enrollments uq_enrollments_source_enrollment_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT uq_enrollments_source_enrollment_id UNIQUE (source_enrollment_id);


--
-- TOC entry 4888 (class 2606 OID 16518)
-- Name: employees fk_employee_department; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT fk_employee_department FOREIGN KEY (department_id) REFERENCES public.departments(department_id);


--
-- TOC entry 4889 (class 2606 OID 16548)
-- Name: enrollments fk_enrollment_employee; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT fk_enrollment_employee FOREIGN KEY (employee_id) REFERENCES public.employees(employee_id);


--
-- TOC entry 4890 (class 2606 OID 16553)
-- Name: enrollments fk_enrollment_plan; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT fk_enrollment_plan FOREIGN KEY (plan_id) REFERENCES public.benefit_plans(plan_id);


-- Completed on 2026-11-19 11:08:28

--
-- PostgreSQL database dump complete
--

\unrestrict S4HZn5M9DiiXqQggC0WztfG7sg5Ms7IgMIeEoasSa18rRZTGkdeA3A5x6YawWys
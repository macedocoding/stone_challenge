CREATE TABLE public.technicians (
                technician_id SERIAL NOT NULL,
                technician_email VARCHAR(50),
                CONSTRAINT technician_id PRIMARY KEY (technician_id)
);
COMMENT ON COLUMN public.technicians.technician_id IS 'Technicians table PK';


CREATE TABLE public.providers (
                provider_id SERIAL NOT NULL,
                provider VARCHAR(100),
                CONSTRAINT provider_id PRIMARY KEY (provider_id)
);
COMMENT ON COLUMN public.providers.provider_id IS 'Providers table PK';


CREATE TABLE public.terminals (
                terminal_id INTEGER NOT NULL,
                provider_id INTEGER NOT NULL,
                technician_id INTEGER NOT NULL,
                terminal_serial_number VARCHAR(36),
                terminal_model VARCHAR(20),
                terminal_type VARCHAR(40),
                CONSTRAINT terminal_id PRIMARY KEY (terminal_id)
);
COMMENT ON COLUMN public.terminals.terminal_id IS 'Terminals table PK';


CREATE TABLE public.customers (
                customer_id VARCHAR(36) NOT NULL,
                customer_phone VARCHAR(14),
                city VARCHAR(50),
                country VARCHAR(50),
                country_state VARCHAR(2),
                zip_code VARCHAR(8),
                street_name VARCHAR(100),
                complement VARCHAR(100),
                neighborhood VARCHAR(100),
                CONSTRAINT customer_id PRIMARY KEY (customer_id)
);
COMMENT ON COLUMN public.customers.customer_id IS 'Customers table PK';


CREATE TABLE public.orders (
                order_id SERIAL NOT NULL,
                customer_id VARCHAR(36) NOT NULL,
                terminal_id INTEGER NOT NULL,
                order_number INTEGER,
                cancellation_reason VARCHAR(255),
                last_modified_date DATE,
                arrival_date DATE,
                deadline_date DATE,
                CONSTRAINT order_id PRIMARY KEY (order_id)
);
COMMENT ON COLUMN public.orders.order_id IS 'Orders table Surrogate Key used as PK.';


ALTER TABLE public.terminals ADD CONSTRAINT stg_technicians_stg_terminals_fk
FOREIGN KEY (technician_id)
REFERENCES public.technicians (technician_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.terminals ADD CONSTRAINT stg_providers_stg_terminals_fk
FOREIGN KEY (provider_id)
REFERENCES public.providers (provider_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.orders ADD CONSTRAINT stg_terminals_stg_orders_fk
FOREIGN KEY (terminal_id)
REFERENCES public.terminals (terminal_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.orders ADD CONSTRAINT stg_customers_stg_orders_fk
FOREIGN KEY (customer_id)
REFERENCES public.customers (customer_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;
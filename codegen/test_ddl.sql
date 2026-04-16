-- Test DDL: 4 Asset domain tables from Database_Schema_Specification.md
-- Used to validate the DDL-to-model generation script.

create table property (
  property_id        uuid primary key default gen_random_uuid(),
  tenant_id          uuid not null references tenant(tenant_id),
  client_id          uuid null references client(client_id),
  portfolio_id       uuid null references portfolio(portfolio_id),
  property_name      text not null,
  street_address     text not null,
  city               text not null,
  state              text not null,
  zip_code           text not null,
  total_units        integer null,
  year_built         integer null,
  property_class     text null,
  building_type      text null,
  buildings_count    integer null,
  stories            integer null,
  total_sqft         integer null,
  lot_size           text null,
  parking_spaces     integer null,
  parking_type       text null,
  is_subject         boolean not null default true,
  latitude           numeric(10,7) null,
  longitude          numeric(10,7) null,
  attributes         jsonb not null default '{}'::jsonb,
  created_at         timestamptz not null default now(),
  updated_at         timestamptz not null default now()
);

create table unit (
  unit_id            uuid primary key default gen_random_uuid(),
  property_id        uuid not null references property(property_id),
  unit_natural_key   text not null,
  created_at         timestamptz not null default now(),
  retired_at         timestamptz null,
  unique (property_id, unit_natural_key)
);

create table unit_version (
  unit_version_id    uuid primary key default gen_random_uuid(),
  unit_id            uuid not null references unit(unit_id),
  valid_from         date not null,
  valid_to           date null,
  building_id        uuid null references building(building_id),
  floor_plan_id      uuid null references floor_plan(floor_plan_id),
  floor_label        text null,
  unit_label         text not null,
  floorplan_code     text null,
  bedrooms           numeric(4,1) null,
  bathrooms          numeric(4,1) null,
  sqft               integer null,
  finish_package     text null,
  attributes         jsonb not null default '{}'::jsonb,
  recorded_from      timestamptz not null default now(),
  recorded_to        timestamptz null
);

create table unit_alias (
  alias_id           uuid primary key default gen_random_uuid(),
  unit_id            uuid not null references unit(unit_id),
  source_system_id   uuid null references source_system(source_system_id),
  alias_key          text not null,
  alias_type         text not null,
  valid_from         date null,
  valid_to           date null,
  match_method       text null,
  match_confidence   numeric(5,4) null,
  reviewer_override  boolean not null default false,
  created_at         timestamptz not null default now()
);

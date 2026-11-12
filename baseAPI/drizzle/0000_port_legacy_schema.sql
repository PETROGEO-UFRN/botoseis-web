CREATE TABLE "commands_table" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar,
	"parameters" text,
	"workflowId" integer,
	"owner_email" varchar,
	"program_id" integer,
	"is_active" boolean
);
--> statement-breakpoint
CREATE TABLE "datasets_table" (
	"id" serial PRIMARY KEY NOT NULL,
	"owner_email" varchar,
	"originWorkflowId" integer
);
--> statement-breakpoint
CREATE TABLE "helper_file_link_table" (
	"id" serial PRIMARY KEY NOT NULL,
	"path" varchar,
	"data_type" varchar,
	"lineId" integer,
	"created_at" timestamp with time zone DEFAULT now(),
	"modified_at" timestamp with time zone
);
--> statement-breakpoint
CREATE TABLE "lines_table" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar,
	"projectId" integer,
	"owner_email" varchar
);
--> statement-breakpoint
CREATE TABLE "ordered_commands_list_table" (
	"id" serial PRIMARY KEY NOT NULL,
	"workflowId" integer,
	"commandIds" integer[]
);
--> statement-breakpoint
CREATE TABLE "parameters_table" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar,
	"description" varchar,
	"input_type" varchar,
	"programId" integer,
	"isRequired" boolean,
	"example" varchar
);
--> statement-breakpoint
CREATE TABLE "program_groups_table" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar,
	"description" varchar
);
--> statement-breakpoint
CREATE TABLE "programs_table" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar,
	"description" varchar,
	"path_to_executable_file" varchar,
	"groupId" integer
);
--> statement-breakpoint
CREATE TABLE "projects_table" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar,
	"userId" uuid,
	"created_at" timestamp with time zone DEFAULT now(),
	"modified_at" timestamp with time zone
);
--> statement-breakpoint
CREATE TABLE "su_file_link_table" (
	"id" serial PRIMARY KEY NOT NULL,
	"path" varchar,
	"projectId" integer,
	"datasetId" integer,
	"created_at" timestamp with time zone DEFAULT now(),
	"modified_at" timestamp with time zone
);
--> statement-breakpoint
CREATE TABLE "users_table" (
	"id" uuid PRIMARY KEY NOT NULL,
	"name" varchar,
	"email" varchar,
	"is_admin" boolean,
	"password" "bytea",
	CONSTRAINT "users_table_email_key" UNIQUE("email")
);
--> statement-breakpoint
CREATE TABLE "workflow_parents_association_table" (
	"workflowId" integer PRIMARY KEY NOT NULL,
	"lineId" integer,
	"projectId" integer,
	"datasetId" integer
);
--> statement-breakpoint
CREATE TABLE "workflows_table" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar,
	"owner_email" varchar,
	"output_name" varchar,
	"input_file_link_id" integer,
	"post_processing_options" text,
	"picks_table_file_id" integer
);
--> statement-breakpoint
ALTER TABLE "commands_table" ADD CONSTRAINT "FK_programs_table_commands_table" FOREIGN KEY ("program_id") REFERENCES "public"."programs_table"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "commands_table" ADD CONSTRAINT "FK_users_table_commands_table" FOREIGN KEY ("owner_email") REFERENCES "public"."users_table"("email") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "commands_table" ADD CONSTRAINT "FK_workflows_table_commands_table" FOREIGN KEY ("workflowId") REFERENCES "public"."workflows_table"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "datasets_table" ADD CONSTRAINT "FK_users_table_dataset_table" FOREIGN KEY ("owner_email") REFERENCES "public"."users_table"("email") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "datasets_table" ADD CONSTRAINT "FK_workflows_tables_datasets_table" FOREIGN KEY ("originWorkflowId") REFERENCES "public"."workflows_table"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "helper_file_link_table" ADD CONSTRAINT "FK_lines_table_helper_file_link_table" FOREIGN KEY ("lineId") REFERENCES "public"."lines_table"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "lines_table" ADD CONSTRAINT "FK_projects_table_lines_table" FOREIGN KEY ("projectId") REFERENCES "public"."projects_table"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "lines_table" ADD CONSTRAINT "FK_users_table_lines_table" FOREIGN KEY ("owner_email") REFERENCES "public"."users_table"("email") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "ordered_commands_list_table" ADD CONSTRAINT "FK_workflows_table_workflow_commands_list_table" FOREIGN KEY ("workflowId") REFERENCES "public"."workflows_table"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "parameters_table" ADD CONSTRAINT "FK_programs_table_parameters_table" FOREIGN KEY ("programId") REFERENCES "public"."programs_table"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "programs_table" ADD CONSTRAINT "FK_program_groups_table_programs_table" FOREIGN KEY ("groupId") REFERENCES "public"."program_groups_table"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "projects_table" ADD CONSTRAINT "FK_users_table_projects_table" FOREIGN KEY ("userId") REFERENCES "public"."users_table"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "su_file_link_table" ADD CONSTRAINT "FK_datasets_table_su_file_link_table" FOREIGN KEY ("datasetId") REFERENCES "public"."datasets_table"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "su_file_link_table" ADD CONSTRAINT "FK_projects_table_su_file_link_table" FOREIGN KEY ("projectId") REFERENCES "public"."projects_table"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "workflow_parents_association_table" ADD CONSTRAINT "FK_workflow_parents_association_table_dataset_table" FOREIGN KEY ("datasetId") REFERENCES "public"."datasets_table"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "workflow_parents_association_table" ADD CONSTRAINT "FK_workflow_parents_association_table_lines_table" FOREIGN KEY ("lineId") REFERENCES "public"."lines_table"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "workflow_parents_association_table" ADD CONSTRAINT "FK_workflow_parents_association_table_projects_table" FOREIGN KEY ("projectId") REFERENCES "public"."projects_table"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "workflow_parents_association_table" ADD CONSTRAINT "FK_workflow_parents_association_table_workflows_table" FOREIGN KEY ("workflowId") REFERENCES "public"."workflows_table"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "workflows_table" ADD CONSTRAINT "FK_helper_file_link_table_workflows_table" FOREIGN KEY ("picks_table_file_id") REFERENCES "public"."helper_file_link_table"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "workflows_table" ADD CONSTRAINT "FK_su_file_links_table_workflows_table" FOREIGN KEY ("input_file_link_id") REFERENCES "public"."su_file_link_table"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "workflows_table" ADD CONSTRAINT "FK_users_table_workflows_table" FOREIGN KEY ("owner_email") REFERENCES "public"."users_table"("email") ON DELETE no action ON UPDATE no action;
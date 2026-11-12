ALTER TABLE "lines_table" DROP CONSTRAINT "FK_projects_table_lines_table";
--> statement-breakpoint
ALTER TABLE "lines_table" DROP CONSTRAINT "FK_users_table_lines_table";
--> statement-breakpoint
ALTER TABLE "parameters_table" DROP CONSTRAINT "FK_programs_table_parameters_table";
--> statement-breakpoint
ALTER TABLE "programs_table" DROP CONSTRAINT "FK_program_groups_table_programs_table";
--> statement-breakpoint
ALTER TABLE "workflow_parents_association_table" DROP CONSTRAINT "FK_workflow_parents_association_table_lines_table";
--> statement-breakpoint
ALTER TABLE "lines_table" ADD CONSTRAINT "FK_projects_table_lines_table" FOREIGN KEY ("projectId") REFERENCES "public"."projects_table"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "lines_table" ADD CONSTRAINT "FK_users_table_lines_table" FOREIGN KEY ("owner_email") REFERENCES "public"."users_table"("email") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "parameters_table" ADD CONSTRAINT "FK_programs_table_parameters_table" FOREIGN KEY ("programId") REFERENCES "public"."programs_table"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "programs_table" ADD CONSTRAINT "FK_program_groups_table_programs_table" FOREIGN KEY ("groupId") REFERENCES "public"."program_groups_table"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "workflow_parents_association_table" ADD CONSTRAINT "FK_workflow_parents_association_table_lines_table" FOREIGN KEY ("lineId") REFERENCES "public"."lines_table"("id") ON DELETE set null ON UPDATE no action;
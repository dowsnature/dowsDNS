#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
	char *input_file_name 		= "data/hosts";
	char *output_file_name 		= "data/rpz.json";
	FILE *input_file_pointer	= fopen(input_file_name,  "r");
	FILE *output_file_pointer	= fopen(output_file_name, "w");
	char input_string[255];
	char *domain, *ip;
	int  is_first = 1;

	if (input_file_pointer == NULL || output_file_pointer == NULL) {
		printf( "文件打开失败\n" );
		return 0;
	}

	fputs( "{", output_file_pointer );

	while (fgets(input_string, sizeof(input_string), input_file_pointer) != NULL) {		
		if (input_string[0] == '#')
			continue;
		ip	 = strtok(input_string, "\n\t ");
		if (ip == NULL)
			continue;
		domain   = strtok(NULL, "\n\t ");
		if (domain == NULL)
			continue;
		if (is_first == 1)
			is_first = 0;
		else
			fputs( ","  , output_file_pointer);
		fputs( "\""  , 	output_file_pointer);
		fputs( domain, 	output_file_pointer);
		fputs( "\""  , 	output_file_pointer);
		fputs( ":"  , 	output_file_pointer);
		fputs( "\""  , 	output_file_pointer);
		fputs( ip, 	output_file_pointer);
		fputs( "\""  ,	output_file_pointer);
	}

	fputs( "}", output_file_pointer );

	fclose(input_file_pointer);
	fclose(output_file_pointer);

	return 0;
}


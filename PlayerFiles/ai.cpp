#include "basic.h"
#include <stdio.h>

game_info info;




Command AI_main()
{
	Command cmd;
	//ѡ��������д�Լ���AI������
	printf("in AI_main\n");
	cmd.order = 0;
	cmd.destination = info.soldier[info.move_id][info.team_number].pos;
	cmd.target_id = 0;
	return cmd;
}
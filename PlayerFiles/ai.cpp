#include "basic.h"

game_info info;




Command AI_main()
{
	Command cmd;
	//ѡ��������д�Լ���AI������
	cmd.order = 0;
	cmd.destination = info.soldier[info.move_id][info.team_number].pos;
	cmd.target_id = 0;
	return cmd;
}
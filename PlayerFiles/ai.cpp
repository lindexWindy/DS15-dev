#include"basic.h"
command AI_main()
{
	command cmd;
	//ѡ��������д�Լ���AI������
	cmd.order = 1;
	cmd.target_id = 0;
	cmd.destination.x = initial.soldier[0][1 - initial.team_number].p.x + 1 ; cmd.destination.y = initial.soldier[0][1 - initial.team_number].p.y + 1;
	return cmd;
}
#include <chewing_cpp/4_3/4_3.hpp>

int main()
{
  if(0)
  {
    Marine marine1(2, 3);
    Marine marine2(3, 5);

    marine1.show_status();
    marine2.show_status();

    std::cout << std::endl << "마린 1 이 마린 2 를 공격! " << std::endl;
    marine2.be_attacked(marine1.attack());

    marine1.show_status();
    marine2.show_status();
  }

  if(0)
  {
    Marine* marines[100];

    marines[0] = new Marine(2, 3, "Marine 2"); //생성자 호출
    marines[1] = new Marine(3, 5, "Marine 1");

    marines[0]->show_status();
    marines[1]->show_status();

    std::cout << std::endl << "마린 1 이 마린 2 를 공격! " << std::endl;

    marines[0]->be_attacked(marines[1]->attack());

    marines[0]->show_status();
    marines[1]->show_status();

    delete marines[0]; // 소멸자 호출
    std::cout << std::endl;
    delete marines[1];
  }

  if(0)//복사 생성자
  {
    Photon_Cannon pc1(3, 3);
    Photon_Cannon pc2(pc1); // 복사 생성자 호출
    Photon_Cannon pc3 = pc2; // 복사 생성자 호출

    pc1.show_status();
    pc2.show_status();
    pc3.show_status();
  }

  if(1)//default 복사 생성자의 한계 -> 직접 만든 복사 생성자 주석 처리
  {
    Photon_Cannon pc1(3, 3, "Cannon");
    Photon_Cannon pc2 = pc1;

    std::cout << &pc1.name << "," << &pc2.name << std::endl;

    pc1.show_status();
    pc2.show_status();
  }

  return 0;
}
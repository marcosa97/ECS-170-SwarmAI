#include <sc2api/sc2_api.h>

#include <iostream>

using namespace sc2;

class Bot : public Agent {
public:
    virtual void OnGameStart() final {
        std::cout << "Hello, World!" << std::endl;
    }

    virtual void OnStep() final {
		const ObservationInterface* obs = Observation();
		//const VitalScoreDetails* score = VitalScoreDetails();
        std::cout << Observation()->GetGameLoop() << std::endl;
		//std::cout << "Minerals: \t" << obs->GetMinerals() << std::endl;
		//std::cout << "Vespene: \t" << obs->GetVespene() << std::endl;
		const Score& score = obs->GetScore();
		//std::cout << score.score_details.collected_minerals << std::endl;
		//std::cout << Observation()->GetScore().float_count << std::endl;//.score_details.collected_minerals << std::endl;
		//std::cout << "Health: \t" << VitalScoreDetails().life
		//std::cout << Observation()->GetUnitTypeData()[1].armor << std::endl;

		struct NotStructure {
			NotStructure(const ObservationInterface* obs) : observation_(obs) {}

			bool operator()(const Unit& unit) {
				auto attributes = observation_->GetUnitTypeData().at(unit.unit_type).attributes;
				for (const auto& attribute : attributes) {
					if (attribute == Attribute::Structure) {
						return false;
					}
				}
			}

			const ObservationInterface* observation_;
		};
		Units unitsSelf = Observation()->GetUnits(Unit::Self, NotStructure(obs));
		Units unitsEnemy = Observation()->GetUnits(Unit::Enemy, NotStructure(obs));
		//holds infor for extractData Self
		float healthSelf[10000];
		float shieldSelf[10000];
		float energySelf[10000];
		//holds info for extractData enemy
		float healthEnemy[10000];
		//holds info for move
		float xposSelf[10000];
		float yposSelf[10000];
		int i = 0;
		for (auto & unit : unitsSelf) {
			healthSelf[i] = unit->health;
			shieldSelf[i] = unit->shield;
			energySelf[i] = unit->energy;
			xposSelf[i] = unit->pos.x;
			yposSelf[i] = unit->pos.y;
			std::cout << unit->health << "\t";
			i++;
		}
		std::cout << "num of unitsSelf is " << i << std::endl;
		int j = 0;
		for (auto & unit : unitsEnemy) {
			healthEnemy[j] = unit->health;
			std::cout << unit->health << "\t";
			j++;
		}
		std::cout << "num of unitsEnemy is " << j << std::endl;
    }
};

void initialize(Coordinator &coordinator) {
	//Coordinator coordinator;
	Bot bot;
	coordinator.SetParticipants({
		CreateComputer(Race::Terran),
		CreateComputer(Race::Protoss)
		});
	coordinator.LaunchStarcraft();
	coordinator.StartGame(sc2::kMapEmpty);
	//GameInfo.width = 1000;
	//GameInfo.height = 750;

}
// Extract two sets of game data, one for ally, one for enemy.This data includes all units in vision and their properties.
void extract_data(){
	//sc2interfaces.h

	//ObservationInterface().GetUnits();
	//ObservationInterface()->GetMinerals();
	//ObservationInterface()->GetVespene();
}
	

int main(int argc, char* argv[]) {
    Coordinator coordinator;
    coordinator.LoadSettings(argc, argv);

    Bot bot;
    coordinator.SetParticipants({
        CreateParticipant(Race::Terran, &bot),
        //CreateComputer(Race::Terran),
		CreateComputer(Race::Zerg)
    });
	//coordinator.SetWindowSize(350, 350);
	//coordinator.SetStepSize(1000);
    coordinator.LaunchStarcraft();
    coordinator.StartGame(sc2::kMapBelShirVestigeLE);
	/*Coordinator coordinator;
	coordinator.LoadSettings(argc, argv);
	initialize(coordinator);
	*/

    while (coordinator.Update()) {
    }

    return 0;
}
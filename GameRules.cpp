//
// Created by loko on 22/11/2025.
//
#include "GameRules.h"
#include "Color.h"

State GameRules::playMove(const State& state,int field, Color color) {
    bool distributing_in_all_holes = false;
    int seeds=0;
    int transparent_seeds=0;
    int score=0;
    State newState=State(state);
    newState.moves_played++;
    if (color==red || color==transparentRED)distributing_in_all_holes=true;
    if (field>=16||field<0) {
        cerr<<"ERROR";
    }
    seeds=newState.board.fields[field].take_seeds(color,transparent_seeds);

    if (seeds==0 && transparent_seeds==0) {
        cerr<<"Your play isn't valid: No seed in the demanded color"<<endl;
    }
    if (field==15) {
        field=0;
    }else {
        field++;
    }


    while (seeds!=0 ||transparent_seeds!=0) {

        if (transparent_seeds!=0) {
            newState.board.fields[field].put_seed(transparentRED);
            transparent_seeds--;
        }else {
            (distributing_in_all_holes)
                ? newState.board.fields[field].put_seed(red)
                : newState.board.fields[field].put_seed(blue);
            seeds--;
        }

        if (distributing_in_all_holes) {
            if (field!=15) {
                field++;
            }else {
                field=0;
            }
        }else {
            if (field==14) {
                field=0;
            }else if (field==15) {
                field=1;
            }else {
                field+=2;
            }
        }
    }
    score=capture(newState,field);
    if (newState.player_playing) {
        newState.score_p1+=score;
    }else {
        newState.score_p2+=score;
    }

    newState.player_playing = !newState.player_playing;
    //Starvation rule
    vector<pair<int,Color>> opponentMoves = getPossibleMoves(newState);

    if (opponentMoves.empty()) {
        int remaining = 0;
        for(int i=0; i<16; i++) {
            remaining += newState.board.fields[i].take_all_seeds();
        }

        if (!newState.player_playing) {
            newState.score_p1 += remaining;
        } else {
            newState.score_p2 += remaining;
        }
    }

    return newState;
}

bool GameRules::gameOver(const State& state) {

    if (state.moves_played>=400) {
        return true;
    }

    if (state.score_p1 >= 49 || state.score_p2 >= 49) {
        return true;
    }
    int seedsOnBoard = 96 - (state.score_p1 + state.score_p2);
    if (seedsOnBoard < 10) {
        return true;
    }

    return false;
}

int GameRules::capture(State& state,int field) {
    bool capture=true;
    int score=0;
    while (capture) {
        if (state.board.fields[field].total_seeds==2 || state.board.fields[field].total_seeds==3) {
            score+=state.board.fields[field].take_all_seeds();

                if (field==0) {
                    field=15;
                }else {
                    field--;
                }
        }else {
            return score;
        }
    }
    return 0;
}

vector<pair<int,Color>> GameRules::getPossibleMoves(const State& state) {
    vector<pair<int,Color>> possible_coups;
    int start;
    (state.player_playing)?start=0:start=1;

    for (int i=start;i<16;i+=2) {
        if (state.board.fields[i].red_seeds>0) {
            possible_coups.push_back(  {i,red});
        }
        if (state.board.fields[i].blue_seeds>0) {
            possible_coups.push_back(  {i,blue});
        }
        if (state.board.fields[i].transparent_seeds>0) {
            possible_coups.push_back(  {i,transparentRED});
            possible_coups.push_back(  {i,transparentBLUE});
        }
    }
    return possible_coups;
}

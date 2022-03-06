pragma solidity >=0.4.22 <0.9.0;

contract Election {

    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }
    
    bool goingon = true;
    address public owner;

    mapping(address => bool) public voters;
    mapping(uint => Candidate) public candidates;
    
    uint public candidatesCount;    
    uint public totalVote = 0;

    constructor () public {
        owner = msg.sender;
        addCandidate("Candidate 1");
        addCandidate("Candidate 2");
        addCandidate("Candidate 3");
    
    }

    function addCandidate (string memory _name) private {
        candidatesCount ++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
    }

    function end () public {
        require(msg.sender == owner , " ONLY OWNER CAN END");
        goingon = false;
    }

    function vote (uint _candidateId) public {
        require(!voters[msg.sender],"Already voted");

        require(_candidateId > 0 && _candidateId <= candidatesCount,"Invalid candidate");

        require(goingon,"Election ended");

        voters[msg.sender] = true;

        candidates[_candidateId].voteCount ++;
        totalVote++;

    }
}
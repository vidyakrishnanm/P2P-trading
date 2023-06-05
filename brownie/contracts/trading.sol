// SPDX-License-Identifier: GPL-3.0

//pragma solidity >=0.8.0 <0.8.15;
pragma solidity ^0.8.0;

pragma experimental ABIEncoderV2;

contract EnergyTrade {
    struct Offer {
        uint32 ID;
        address seller;
        address buyer;
        uint32 energy;
        uint32 price;
        uint256 OfferedTime;
        uint256 S2BPaidTime;
        bool choosed;
        bool confirm_buyer;
        bool confirm_seller;
        bool delivered;
    }
    mapping(uint256 => Offer) public offers;
    uint32 public offerID;
    uint256 count;
    uint256[] data;
    uint256[] dataList;

    function addOffer(uint32 energy, uint32 price) public {
        Offer storage newOffer = offers[offerID];
        newOffer.ID = offerID;
        newOffer.seller = msg.sender;
        newOffer.energy = energy;
        newOffer.price = price;
        newOffer.OfferedTime = block.timestamp;
        newOffer.choosed = false;
        newOffer.confirm_buyer = false;
        newOffer.confirm_seller = false;
        newOffer.delivered = false;
        offerID += 1;
    }

    function ChooseOffer(uint32 id) public {
        offers[id].choosed = true;
    }

    function confirmTx_S2B(uint32 id) public {
        offers[id].confirm_buyer = true;
        offers[id].buyer = msg.sender;
        offers[id].S2BPaidTime = block.timestamp;
    }

    function finalDelivery(uint32 id) public {
        offers[id].delivered = true;
    }

    function confirmTx_B2S(uint32 id) public {
        offers[id].confirm_seller = true;
        //offers[id].Hash_B2S = Hash_B2S;
    }

    function retreive_offer_by_id(
        uint32 id
    ) public view returns (uint32, uint32) {
        Offer storage derivedOffer = offers[id];
        return (derivedOffer.energy, derivedOffer.price);
    }

    function retreive_final_details(
        uint32 id
    ) public view returns (Offer memory) {
        return offers[id];
    }

    function getOfferData() internal view returns (uint256[] memory) {
        uint256[] memory dataList = new uint256[](offerID * 3); // allocate memory for maximum possible size
        uint256 dataIndex = 0;
        for (uint256 i = 0; i < offerID; i++) {
            if (!offers[i].delivered) {
                Offer storage derivedOffer = offers[i];
                dataList[dataIndex] = i;
                dataList[dataIndex + 1] = derivedOffer.energy;
                dataList[dataIndex + 2] = derivedOffer.price;
                dataIndex += 3;
            }
        }
        // Trim the dataList array to the actual size
        uint256[] memory trimmedData = new uint256[](dataIndex);
        for (uint256 i = 0; i < dataIndex; i++) {
            trimmedData[i] = dataList[i];
        }
        return trimmedData;
    }

    function listOffers() public view returns (uint256[] memory) {
        return getOfferData();
    }
}

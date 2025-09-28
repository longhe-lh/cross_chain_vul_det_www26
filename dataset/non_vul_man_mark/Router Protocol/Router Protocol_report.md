# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Deposit1, stake2
- **rel_chain**: voteProposal, executeProposal, cancelProposal
- **det_chain**: Settlement1, Unstake2
### src_chain: Ethereum
- **事件**: Deposit1
  - 函数: deposit
  - 关键操作: _deposit(destinationChainID, resourceID, data, distribution, flags, path, feeTokenAddress)
- **事件**: stake2
  - 函数: stake
  - 关键操作: ILiquidityPool depositHandler = ILiquidityPool(handler);, depositHandler.stake(msg.sender, tokenAddress, amount);
### rel_chain: RelayChain
- **事件**: voteProposal
  - 函数: voteProposal
  - 关键操作: bytes32 proposalHash = keccak256(abi.encodePacked(chainID, depositNonce, dataHash));, _voter.vote(_proposals[proposalHash], 1, msg.sender);
- **事件**: executeProposal
  - 函数: executeProposal
  - 关键操作: IERC20Upgradeable handler = IERCHandler(_resourceIDToHandlerAddress[resourceID]);, (settlementToken, swapDetails.returnAmount) = depositHandler.executeProposal(swapDetails, resourceID);
- **事件**: cancelProposal
  - 函数: cancelProposal
  - 关键操作: require(currentStatus == IVoterUpgradeable.ProposalStatus.Active || currentStatus == IVoterUpgradeable.ProposalStatus.Passed, "Proposal cannot be cancelled");, _voter.setStatus(_proposals[proposalHash]);
### det_chain: BinanceSmartChain
- **事件**: Settlement1
  - 函数: executeProposal
  - 关键操作: emit Settlement(chainID, depositNonce, settlementToken, swapDetails.returnAmount, IVoterUpgradeable.ProposalStatus.Executed);, emit ProposalEvent(chainID, depositNonce, IVoterUpgradeable.ProposalStatus.Executed, dataHash);
- **事件**: Unstake2
  - 函数: unstake
  - 关键操作: ILiquidityPool depositHandler = ILiquidityPool(handler);, depositHandler.unstake(msg.sender, tokenAddress, amount);
---

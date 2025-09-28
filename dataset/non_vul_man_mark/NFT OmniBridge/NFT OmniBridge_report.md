# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokensBridgingInitiated1
- **rel_chain**: UserRequestForAffirmation, UserRequestForSignature, CollectedSignatures, AffirmationCompleted, RelayedMessage
- **det_chain**: TokensBridged1
### src_chain: ForeignNFTOmnibridge
- **事件**: TokensBridgingInitiated1
  - 函数: bridgeSpecificActionsOnTokenTransfer
  - 关键操作: if (!isTokenRegistered(_token)) { _setNativeTokenIsRegistered(_token, REGISTERED); }, bytes memory data = _prepareMessage(_token, _receiver, _tokenIds, _values);, bytes32 _messageId = _passMessage(data, _isOracleDrivenLaneAllowed(_token, _from, _receiver));, _recordBridgeOperation(_messageId, _token, _from, _tokenIds, _values);
### rel_chain: AMB Bridge
- **事件**: UserRequestForAffirmation
  - 函数: requireToPassMessage
- **事件**: UserRequestForSignature
  - 函数: requireToConfirmMessage
- **事件**: CollectedSignatures
  - 函数: collectedSignatures
- **事件**: AffirmationCompleted
  - 函数: affirmationCompleted
- **事件**: RelayedMessage
  - 函数: relayedMessage
### det_chain: ForeignNFTOmnibridge
- **事件**: TokensBridged1
  - 函数: _handleTokens
  - 关键操作: require(isTokenExecutionAllowed(_token));, _releaseTokens(_token, _isNative, _recipient, _tokenIds, _values);, emit TokensBridged(_token, _recipient, _tokenIds, _values, messageId());
---

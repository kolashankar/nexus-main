import React from "react";
import { jsx as _jsx } from "react/jsx-runtime";
import { Component } from 'react';
import { ErrorFallback } from './ErrorFallback';
import { logError } from '../../../utils/error-handlers';
export class RetryBoundary extends Component {
    constructor(props) {
        super(props);
        Object.defineProperty(this, "handleRetry", {
            enumerable: true,
            configurable: true,
            writable: true,
            value: () => {
                const { maxRetries = 3 } = this.props;
                const { retryCount } = this.state;
                if (retryCount < maxRetries) {
                    this.setState({
                        hasError: false,
                        error: null,
                        retryCount: retryCount + 1,
                    });
                }
                else {
                    // Max retries reached, reload page
                    window.location.reload();
                }
            }
        });
        this.state = {
            hasError: false,
            error: null,
            retryCount: 0,
        };
    }
    static getDerivedStateFromError(error) {
        return {
            hasError: true,
            error,
            retryCount: 0,
        };
    }
    componentDidCatch(error, errorInfo) {
        logError(error, {
            componentStack: errorInfo.componentStack,
            retryCount: this.state.retryCount,
        });
        if (this.props.onError) {
            this.props.onError(error, errorInfo);
        }
    }
    render() {
        const { hasError, error } = this.state;
        const { children, fallback } = this.props;
        if (hasError && error) {
            if (fallback) {
                return fallback(error, this.handleRetry);
            }
            return (_jsx(ErrorFallback, { error: error, resetErrorBoundary: this.handleRetry }));
        }
        return children;
    }
}
